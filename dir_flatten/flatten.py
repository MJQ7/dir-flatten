import os
import dir_flatten.globe
from dir_flatten.df import DF
from dir_flatten.ui import UI
from dir_flatten.logger import Logger
from rich.live import Live
from rich.prompt import Prompt

def flatten():
    dir_flatten.globe.TLDN = Prompt.ask("Enter the directory to flatten:", default=os.getcwd())
    UI.create_ui()
    Logger.create(UI.layout)

    files_in_directory = DF.get_files_in_directory(dir_flatten.globe.TLDN)
    if not files_in_directory:
        return
    
    files_found = len(files_in_directory)

    MAIN_TASK = UI.progress.add_task("[cyan]Flattening...", total=files_found)

    # Start the Live display with the layout
    with Live(UI.layout, console=UI.console, refresh_per_second=30) as live:
        # Iterate over each file, simulate processing
        for file in files_in_directory:
            DF.process_file(file, dir_flatten.globe.TLDN)  # Process the file
            UI.progress.update(MAIN_TASK, advance=1)  # Update progress

        Logger.write("[green]Flattening complete!")
        Logger.write("[cyan]Cleaning up directories...")
        DF.cleanup_dirs()
        Logger.write("[green]Cleanup complete!")

        files_after_move = DF.get_files_in_directory(dir_flatten.globe.TLDN)

        Logger.write("[cyan]Files found: " + str(files_found))
        Logger.write("[cyan]Files after move: " + str(len(files_after_move)))

        if files_found == len(files_after_move):
            Logger.write("[green]All files moved successfully!")
        else:
            Logger.write("[red]Some files were not moved!")
            Logger.write("[yellow]Determining lost files...")

            lost_files = [file for file in files_in_directory if file not in files_after_move]
            for file in lost_files:
                Logger.write("[red]Lost file: [white]" + file)
            Logger.write("[red]oops...")
            