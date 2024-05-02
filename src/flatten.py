from src.Config import Config
from src.df import DF
from src.ui import UI
from src.logger import Logger
from rich.live import Live

def summary(initial_count, final_count, initial_files, final_files):
    Logger.write(f"[cyan]Files found: {initial_count}")
    Logger.write(f"[cyan]Files after move: {final_count}")
    if initial_count == final_count:
        Logger.write("[green]All files moved successfully!")
    else:
        Logger.write("[red]Some files were not moved!")
        Logger.write("[yellow]Determining lost files...")
        lost_files = [file for file in initial_files if file not in final_files]
        for file in lost_files:
            Logger.write(f"[red]Lost file: [white]{file}")
        Logger.write("[red]oops...")

def flatten():
    files_in_directory = DF.get_files_in_directory(Config.TLDN)
    if not files_in_directory:
        return

    files_found = len(files_in_directory)
    MAIN_TASK = UI.progress.add_task("[cyan]Flattening...", total=files_found)

    with Live(UI.layout, console=UI.console, refresh_per_second=30):
        for file in files_in_directory:
            DF.process_file(file, Config.TLDN)
            UI.progress.update(MAIN_TASK, advance=1)
        Logger.write("[green]Flattening complete!")
        DF.cleanup()

        files_after_move = DF.get_files_in_directory(Config.TLDN)
        summary(files_found, len(files_after_move), files_in_directory, files_after_move)
