# Think of something you melt
import os
import shutil

from dotenv import load_dotenv

load_dotenv()

source_folder = os.environ.get('SOURCE_FOLDER')

for file_name in os.listdir(source_folder):

    source = f"{source_folder}/{file_name}"
    if os.path.isfile(source):
        try:
            file_name.split(".")[1]
        except IndexError:
            extension = "other"
        else:
            extension = file_name.split(".")[-1]

        destination = f"{source_folder}/{extension}/{file_name}"

        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            os.mkdir(f"{source_folder}/{extension}")
            shutil.move(source, destination)
        finally:
            print(f"Moved: {file_name}")


