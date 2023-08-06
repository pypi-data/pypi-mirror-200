import asyncio
from tasktools.taskloop import TaskLoop
from dataclasses import dataclass, field
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler, FileModifiedEvent
from rich import print
from datetime import datetime
from enum import IntEnum, auto
import tomli
from typing import Dict, Any
from .dbdata import DBData

class FileStep(IntEnum):
    EXIST = auto()#1
    START = auto()#2
    CHECK = auto()#3
    READ = auto()#4

class Event(FileSystemEventHandler):
    def __init__(self,
                   loop:asyncio.BaseEventLoop,
                   queue:asyncio.Queue, 
                   *args,**kwargs 
                   ):
        self.loop = loop
        self.queue = queue
        super(*args, **kwargs)

    def on_modified(self, event:FileSystemEvent):
        if type(event)==FileModifiedEvent:
            control = FileStep.READ
            self.loop.call_soon_threadsafe(self.queue.put_nowait, control)


@dataclass
class SettingsFile:
    settings: Path
    data: Dict[str, Any] = field(default_factory=dict)
    unique: bool = False
    delta:int = 10
    not_debug: bool=True
    destiny_change: bool = True
    origin_change: bool = True

    async def run(self, first, queue, control, *args, **kwargs):
        if control == FileStep.EXIST and self.settings.exists():
            control = FileStep.START
            if first:
                control = FileStep.READ

        if control  ==  FileStep.START:
            self.observer.start()
            control = FileStep.CHECK
        
        if control == FileStep.CHECK:
            if not queue.empty():
                for _ in range(queue.qsize()):
                    control = await queue.get()

        if control == FileStep.READ:
            try:
                # then got to check
                old_destiny = self.destiny
                old_origin = self.origin

                txt = self.settings.read_text()
                try:
                    data = tomli.loads(txt)
                    self.set_data(data)

                    if "delta_time" in data:
                        value = data["delta_time"]["value"]
                        if isinstance(value, int):
                            self.delta = value                     

                    if old_origin != self.origin:
                        self.origin_change = True

                    if old_destiny != self.destiny:
                        self.origin_change = True

                    control = FileStep.CHECK
                    if first:
                        first = False
                except Exception as e:
                    # log exception to control possible errors
                    control = FileStep.READ
                    await asyncio.sleep(self.delta)

                # log data registrado 
                print(data)
            except FileNotFoundError as fe:
                print("Archivo no encontrado")
                self.observer.stop()
                control = FileStep.START

        print(f"Wait settings, {self.delta}")
        await asyncio.sleep(self.delta)
        return [first, queue, control, *args], kwargs

    def set_data(self, data):
        self.data = data


    @property
    def days(self):
        """
        Fecha final, dias hacia atras
        """
        return self.data.get("days",7)

    @property
    def hours(self):
        """
        Fecha final, dias hacia atras
        """
        return self.data.get("hours",24)

    @property
    def name(self):
        return self.data.get("app_name")

    @property
    def origins(self):
        return {k:DBData(**v) for k, v in self.data.get("origins",{}).items()}

    @property
    def destinies(self):
        return {k:DBData(**v) for k, v in
                self.data.get("destinies",{}).items()}

    @property
    def destiny_default(self):
        return self.data.get("destiny", "atlas")

    @property
    def origin_default(self):
        return self.data.get("origin", "bellaco")

    @property
    def origin(self):
        return self.origins.get(self.origin_default)

    @property
    def destiny(self):
        return self.destinies.get(self.destiny_default)
    
    def start_date(self):
        sdate  = self.data.get("date")
        dt = sdate.get("start", "2022-10-01")
        format = sdate.get("format", "%Y-%m-%d")
        return datetime.strptime(dt, format)


    def check_source(self)->bool:
        """
        Revisar si conecta un ping, si es correcta
        """
        pass

    def __post_init__(self):
        self.create_task()

    def create_task(self):
        self.observer = Observer()
        queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        self.event_handler = Event(loop, queue)
        self.observer.schedule(
            self.event_handler,
            self.settings,
            recursive=True)
        self.observer.start()
        control = FileStep.EXIST
        first = True
        task = TaskLoop(self.run, [first, queue, control, ], {})
        task.create()
        if not loop.is_running() and self.unique:
            loop.run_forever()

