import typer
import asyncio
from pathlib import Path
from rich import print
from .settings_manager import SettingsFile
from .backup_worker import BackupWorker

app = typer.Typer()

@app.command()
def run(settings:Path, debug:bool=True):
    if settings.exists():
        loop = asyncio.get_event_loop()
        file = SettingsFile(
            settings,
            unique=False,
            not_debug=not debug)
        backup = BackupWorker(
            settings=file)
        backup.run()
        if not loop.is_running():
            loop.run_forever()
    else:
        print("No existe")

if __name__ == "__main__":
    app()
