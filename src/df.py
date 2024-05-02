import os
import shutil
import time
from src.Config import Config
from src.logger import Logger
from rich import print

class DF():

    LOGGER = Logger.get()

    @staticmethod
    def cleanup():
        Logger.write("[cyan]Cleaning up directories...")
        for root, dirs, files in os.walk(Config.TLDN):
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        Logger.write("[green]Cleanup complete!\n")

    @staticmethod
    def remove_bad_files(files):
        to_remove = 'Thumbs.db'
        return [file for file in files if to_remove not in file]

    @staticmethod
    def get_files_in_directory(directory):
        files = []

        if not os.path.isdir(directory):
            print(f"[red]The directory {directory} does not exist.")
            return
        try:
            for root, dirs, files_in_dir in os.walk(directory):
                files.extend(os.path.join(root, file) for file in files_in_dir)
            if not files:
                print("[red]No files found in the directory!")
                return []

        except Exception as e:
            print(f"[red]An error occurred: {e}")
            return []
        return DF.remove_bad_files(files)

    @staticmethod
    def move_file_to_top(file, dir):
        file_name = os.path.basename(file)
        try:
            if('header' in file):
                os.rename(file, os.path.join(dir, 'header_' + file_name))
                DF.LOGGER.write("[yellow]Moved [white]" + file)
            else:
                os.rename(file, os.path.join(dir, file_name))
                DF.LOGGER.write("[green]Moved [white]" + file)
        except FileExistsError:
            DF.LOGGER.write("[yellow]WARN - Already Exists [white]" + file)
            os.rename(file, os.path.join(dir, '1_' + file_name))

    @staticmethod
    def process_file(file, dir):
        DF.move_file_to_top(file, dir)
        time.sleep(0.1)