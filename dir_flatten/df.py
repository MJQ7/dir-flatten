import os
import shutil
import time
import dir_flatten.globe

class DF():

    LOGGER = None

    def __init__(self, logger):
        self.LOGGER = logger

    def cleanup_dirs(self):
        for root, dirs, files in os.walk(dir_flatten.globe.TLDN):
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))  # remove directory

    def remove_bad_files(files):
        to_remove = 'Thumbs.db'
        return [file for file in files if to_remove not in file]

    def get_files_in_directory(self, directory):
        # List to store file names
        files = []
        # Walk through the directory
        for root, dirs, files_in_dir in os.walk(directory):
            for file in files_in_dir:
                files.append(os.path.join(root, file))
        cleaned = DF.remove_bad_files(files)
        return cleaned

    def move_file_to_top(self, file, dir):
        # Get the file name
        file_name = os.path.basename(file)
        # Get the directory name
        try:
            # Move the file to the top level directory
            if('header' in file):
                os.rename(file, os.path.join(dir, 'header_' + file_name))
                self.LOGGER.write("[yellow]Moved [white]" + file)
            else:
                os.rename(file, os.path.join(dir, file_name))
                self.LOGGER.write("[green]Moved [white]" + file)
        except FileExistsError:
            self.LOGGER.write("[yellow]WARN - Already Exists [white]" + file)
            os.rename(file, os.path.join(dir, '1_' + file_name))

    def process_file(self, file, dir):
        DF.move_file_to_top(self, file, dir)
        time.sleep(0.1)