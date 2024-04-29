import os
from DirectoryFunctions import DF as DF
from UI import UI
from Logger import Logger
from rich.live import Live
from rich.prompt import Prompt
from rich.tree import Tree

TLDN = os.getcwd()
UI.create_ui()
UI = UI()
Logger.create(UI.layout)
logger = Logger()
DF = DF(logger)

files_in_directory = DF.get_files_in_directory(TLDN)
files_found = len(files_in_directory)

MAIN_TASK = UI.progress.add_task("[cyan]Flattening...", total=files_found)

# Start the Live display with the layout
with Live(UI.layout, console=UI.console, refresh_per_second=30) as live:

    # Iterate over each file, simulate processing
    for file in files_in_directory:
        DF.process_file(file, TLDN)  # Process the file
        UI.progress.update(MAIN_TASK, advance=1)  # Update progress

    logger.write("[green]Flattening complete!")
    logger.write("[cyan]Cleaning up directories...")
    DF.cleanup_dirs()
    logger.write("[green]Cleanup complete!")

    files_after_move = DF.get_files_in_directory(TLDN)

    logger.write("[cyan]Files found: " + str(files_found))
    logger.write("[cyan]Files after move: " + str(len(files_after_move)))

    if files_found == len(files_after_move):
        logger.write("[green]All files moved successfully!")
    else:
        logger.write("[red]Some files were not moved!")
        logger.write("[yellow]Determining lost files...")

        lost_files = [file for file in files_in_directory if file not in files_after_move]
        for file in lost_files:
            logger.write("[red]Lost file: [white]" + file)
        logger.write("[red]oops...")