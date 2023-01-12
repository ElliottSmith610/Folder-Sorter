import os
import shutil

from dotenv import load_dotenv

load_dotenv()

source_folder = os.environ.get('SOURCE_FOLDER')

pictures = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "psd"]
audio = ["pcm", "wav", "aiff", "mp3", "aac", "ogg", "wma", "flac", "alac"]
video = ["mp4", "mov", "wmv", "webm", "avi", "flv", "mkv", "mts", "mpeg4"]
docs = ["txt", "doc", "docx", "rtf", "pdf"]
apps = ["exe", "zip", "rar", "jar"]

directories = {
    "pictures": pictures,
    "audio": audio,
    "video": video,
    "docs": docs,
    "apps-zips": apps,
}

for file_name in os.listdir(source_folder):

    source = f"{source_folder}/{file_name}"
    if os.path.isfile(source):

        folder = None
        extension = None

        try:
            file_name.split(".")[1]
        except IndexError:
            folder = "other"
        else:
            extension = file_name.split(".")[-1]

            folder = "other"
            for key, value in directories.items():
                if extension.lower() in directories[key]:
                    folder = key

            if folder == "other":
                extension = None

        if folder is None:
            destination = f"{source_folder}/{file_name}"
        elif extension is None:
            destination = f"{source_folder}/{folder}/{file_name}"
        else:
            destination = f"{source_folder}/{folder}/{extension}/{file_name}"

        try:
            shutil.move(source, destination)
        except FileNotFoundError:

            if extension is None:
                os.mkdir(f"{source_folder}/{folder}")
                shutil.move(source, destination)
            else:

                try:
                    os.mkdir(f"{source_folder}/{folder}/{extension}")
                except FileNotFoundError:
                    os.mkdir(f"{source_folder}/{folder}")
                    os.mkdir(f"{source_folder}/{folder}/{extension}")
                finally:
                    shutil.move(source, destination)

        finally:
            print(f"Moved: {file_name}")


