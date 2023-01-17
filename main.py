import os
import shutil
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel, showerror, showinfo

FOLDER = None
TEXT = """Sorts all files in a folder into 6 separate folders if the appropiate file exists.

/Apps          .exe/.zip/.rar/.jar
/Pictures      .jpg/.jpeg/.png/.bmp/.gif/.tiff/.psd/.webp
/Audio         .pcm/.wav/.aiff/.mp3/.aac/.ogg/.wma/.flac/.alac
/Video         .mp4/.mov/.wmv/.webm/.avi/.flv/.mkv/.mts/.mpeg4
/Docs          .txt/.doc/.docx/.rtf/.pdf
/Other         Any extension not listed above
"""

pictures = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "psd", "webp"]
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


def file_sort(source_folder):
    num_files = 0
    for file_name in os.listdir(source_folder):

        source = f"{source_folder}/{file_name}"
        if os.path.isfile(source):

            num_files += 1
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

            if extension is None or not into_sub.get():
                destination = f"{source_folder}/{folder}/{file_name}"
            else:
                destination = f"{source_folder}/{folder}/{extension}/{file_name}"

            try:
                shutil.move(source, destination)
            except FileNotFoundError:

                if extension is None or not into_sub.get():
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

            # finally:
            #     print(f"Moved: {file_name}")
    return num_files


def select_folder():
    global FOLDER
    FOLDER = askdirectory()
    t = "/".join(FOLDER.split("/")[-2:])
    choose_folder_string.config(text=t)


def sort_folder():
    if FOLDER is None:
        showerror(title="Error", message="No Folder selected")
        return
    confirm = askokcancel(title="Confirm Folder Organise", message=f"Are you sure you want to organise\n{FOLDER} ?")
    if confirm:
        num_files = file_sort(FOLDER)
        if num_files > 0:
            showinfo(title="Task Complete", message=f"{num_files} successfully organised!")
        else:
            showerror(title="Oops!", message="No files found in folder")


window = Tk()
window.title = "Folder Organiser"
window.config(padx=30, pady=30)
window.maxsize(600, 600)

title = Label(text="Folder Organiser", font=("Arial", 18, "normal"))
title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
description = Label(text=TEXT, justify=LEFT)
description.grid(row=1, column=0, columnspan=2)
choose_folder_string = Label(font=("Arial", 13, "normal"))
choose_folder_string.grid(row=2, column=0, columnspan=2)
choose_folder = Button(text="Choose Folder", command=select_folder)
choose_folder.grid(row=3, column=0, padx=(0, 300), pady=(10, 0))

into_sub = BooleanVar()
extensions = Checkbutton(text="Sort Extensions into Subfolders\ne.g. Audio/mp3/file.mp3",
                         onvalue=True, offvalue=False, variable=into_sub)
extensions.grid(row=4, column=0, padx=(0, 200), pady=(10, 0))
sort_button = Button(text="Organise Folder", command=sort_folder)
sort_button.grid(row=5, column=0, padx=(0, 300), pady=(10, 0))


window.mainloop()