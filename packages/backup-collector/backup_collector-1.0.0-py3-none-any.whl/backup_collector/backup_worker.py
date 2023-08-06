import asyncio
from dataclasses import dataclass
from pathlib import Path
from rich import print
from datetime import datetime, timedelta
from enum import IntEnum, auto
from tasktools.taskloop import TaskLoop
from .settings_manager import SettingsFile
#from .read_data import read_csv, Mode, load_stations
from .dbsteps import DBStep, DBSend
from data_rdb import Rethink_DBS
from rethinkdb import RethinkDB
from networktools.time import get_datetime_di

from typing import Optional, List  # python 3.9.2
import pytz
local = pytz.timezone("America/Santiago")

rdb = RethinkDB()

KEY = "DT_GEN"
FILTER_OPT = {'left_bound': 'open', 'index': KEY}
DAYS = 7.0
HOURS = 24.0
DATA_LIMIT = 100_000
STEP = 1


def tramos(inicio, final, horas=3):
    lista = []
    tiempo = inicio
    tiempo_last = inicio + timedelta(hours=horas)

    while tiempo <= final:
        tiempo_last = tiempo + timedelta(hours=horas)
        lista.append((tiempo, tiempo_last))
        tiempo = tiempo_last
    return lista


@dataclass
class BackupWorker:
    settings: SettingsFile

    @property
    def days(self):
        """
        Fecha final, dias hacia atras
        """
        return self.settings.days or DAYS

    @property
    def hours(self):
        """
        Fecha final, dias hacia atras
        """
        return self.settings.hours or HOURS

    @property
    def destiny(self):
        return self.settings.destiny

    @property
    def origin(self):
        return self.settings.origin

    @property
    def sleep(self):
        return self.hours*60*60

    @property
    def days_seconds(self):
        return self.days*24*60*60

    def start_date(self):
        naive = self.settings.start_date() or datetime(2022, 10, 1)
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        # CONSTANTES
        return utc_dt

    async def transfer_data(self,
                            di: datetime,
                            control_origin: DBStep,
                            origin: Optional[Rethink_DBS],
                            control_destiny: DBSend,
                            destiny: Optional[Rethink_DBS],
                            tables: List[str],
                            *args,
                            **kwargs):

        print("Transfer data, esperar segundos:", self.sleep)
        if not di:
            control = True
            while control:
                try:
                    di = self.start_date()
                    control = False
                except:
                    print("Failed to read settings")
                    await asyncio.sleep(1)

        if self.settings.destiny_change:
            control_destiny = DBSend.CREATE
            if destiny:
                await destiny.close()
                del destiny
                origin = None

        if self.settings.origin_change:
            control_origin = DBStep.CREATE
            if origin:
                await origin.close()
                del origin
                origin = None

        raw_df = get_datetime_di(delta=self.days_seconds)
        lista_tramos = tramos(di, raw_df, horas=STEP)
        df = rdb.iso8601(raw_df)

        # create instances
        if control_origin == DBStep.CREATE:
            opts = self.origin.dict()
            kwargs["origin_db"] = self.origin
            origin = Rethink_DBS(**opts)
            control_origin = DBStep.CONNECT

        if control_destiny == DBSend.CREATE:
            opts = self.destiny.dict()
            kwargs["destiny_db"] = self.destiny
            destiny = Rethink_DBS(**opts)
            control_destiny = DBSend.CONNECT

        if control_origin == DBStep.CONNECT:
            try:
                await asyncio.wait_for(
                    origin.async_connect(),
                    timeout=10)
                await origin.list_dbs()
                await origin.list_tables()
                tables = [n for n in origin.tables.get("collector")]
                control_origin = DBStep.COLLECT
            except asyncio.TimeoutError as te:
                control_origin = DBStep.CONNECT

        if control_destiny == DBSend.CONNECT:
            try:
                await asyncio.wait_for(
                    destiny.async_connect(),
                    timeout=10)
                await destiny.list_dbs()
                await destiny.list_tables()
                dbname = self.destiny.dbname
                if dbname not in destiny.dblist:
                    await destiny.create_db(dbname)
                # create the difference
                if (difference := set(origin.tables.get("collector")) - set(destiny.tables.get("collector"))):
                    # create
                    for name in difference:
                        await destiny.create_table(name)
                        await destiny.create_index(name, KEY)
                control_destiny = DBSend.SEND
            except asyncio.TimeoutError as te:
                control_destiny = DBSend.CONNECT

        if control_origin == DBStep.COLLECT and control_destiny == DBSend.SEND:
            for table_name in tables:
                try:
                    for (ndi, ndf) in lista_tramos:
                        cursor = await origin.get_data_filter(
                            table_name,
                            [ndi, ndf],
                            FILTER_OPT,
                            KEY)
                        if cursor:
                            lista_oid = [c.get('id') for c in cursor]
                            if self.settings.not_debug:
                                if table_name != "log":
                                    await destiny.save_data(table_name, cursor)
                                for oid in lista_oid:
                                    await origin.delete(oid, table_name)
                            else:
                                print("Borrando....(debug mode)", len(lista_oid))

                    di = df
                except asyncio.exceptions.CancelledError as es:

                    print(f"Falla al consultar tabla {table_name}",
                          [di, df])

                    raise es
        # obtener desde origin por cada tabla, los datos anteriores 'days' hacia
        # atras
        # guardar en destino cada dato en su tabla correspondiente
        await asyncio.sleep(self.sleep)
        return [
            di,
            control_origin,
            origin,
            control_destiny,
            destiny,
            tables,
            *args
        ], kwargs

    def run(self):
        loop = asyncio.get_event_loop()
        control_origin = DBStep.CREATE
        control_destiny = DBSend.CREATE
        tables = []
        di = None
        task = TaskLoop(self.transfer_data, [di, control_origin, None,
                                             control_destiny, None,
                                             tables], {})
        task.create()
        if not loop.is_running():
            loop.run_forever()
