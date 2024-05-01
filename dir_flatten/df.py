import os
import shutil
import time
import dir_flatten.globe
from dir_flatten.logger import Logger
from rich import print

class DF():

    LOGGER = Logger.get()

    @staticmethod
    def cleanup_dirs():
        for root, dirs, files in os.walk(dir_flatten.globe.TLDN):
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))  # remove directory

    @staticmethod
    def remove_bad_files(files):
        to_remove = 'Thumbs.db'
        return [file for file in files if to_remove not in file]

    @staticmethod
    def get_files_in_directory(directory):
        # List to store file names 
        files = []
        if not os.path.isdir(directory):
            print(f"[red]The directory {directory} does not exist.")
            return []
        try:
            # Walk through the directory 
            for root, files_in_dir in os.walk(directory):
                for file in files_in_dir:
                    files.append(os.path.join(root, file))
        except Exception as e:
            print(f"[red]An error occurred: {e}")
            return []
        cleaned = DF.remove_bad_files(files)
        return cleaned

    @staticmethod
    def move_file_to_top(file, dir):
        # Get the file name
        file_name = os.path.basename(file)
        # Get the directory name
        try:
            # Move the file to the top level directory
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