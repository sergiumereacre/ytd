# Importing packages needed.
import tkinter as tk
from tkinter import filedialog
import customtkinter
import requests
from pytube import YouTube
from PIL import Image, ImageTk

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Global variables
        self.ytLink = None
        self.ytObject = None
        self.video = None
        self.location = None
        self.downloadedThumbnail = None

        # App window configurations.
        self.geometry("700x500")
        self.title("Youtube Downloader")
        self.resizable('false', 'false')

        # App window theme.
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")

        # Creating a 2x5 grid.
        self.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Thumbnail of link.
        self.thumbnailImage = customtkinter.CTkImage(Image.open("images/thumbnail.png"), size=(352, 240))
        self.thumbnail = customtkinter.CTkLabel(self, text="", image=self.thumbnailImage)
        self.thumbnail.grid(row=0, column=0, columnspan=2)

        # Text bard on the app.
        self.text = customtkinter.CTkLabel(self, text="Insert a youtube video url link.")
        self.text.grid(row=1, column=0, columnspan=2)

        # Link input
        self.url_var = tk.StringVar()
        self.link = customtkinter.CTkEntry(self, width=400, height=40, textvariable=self.url_var)
        self.link.grid(row=2, column=0, columnspan=2)

        # Main button.
        self.button = customtkinter.CTkButton(self, text="Select Video", command=self.info, height=40, width=100)
        self.button.grid(row=3, column=0, padx=(200, 20), sticky="ew")

        # Download location button.
        self.directoryImage = customtkinter.CTkImage(Image.open("images/folder.png"), size=(30, 30))
        self.locationButton = customtkinter.CTkButton(self, text="", image=self.directoryImage, command=self.downloadLocation, height=30, width=40)
        self.locationButton.grid(row=3, column=1, padx=(0, 200), sticky="ew")

        # Progress percentage
        self.progressBar = customtkinter.CTkProgressBar(self, height=10, width=500)
        self.progressBar.set(0)
        self.progressBar.grid(row=4, column=0, columnspan=2, padx=40, sticky="ew")

    # Get YouTube video information.
    def info(self):
        try:
            # Calling YouTube information.
            self.ytLink = self.link.get()
            self.ytObject = YouTube(self.ytLink, on_progress_callback=self.on_progress)
            # Changes title to YouTube video.
            self.text.configure(text=self.ytObject.title)
            # Changes thumbnail to YouTube video thumbnail.
            self.downloadedThumbnail = customtkinter.CTkImage(Image.open(requests.get(self.ytObject.thumbnail_url, stream=True).raw), size=(352, 240))
            self.thumbnail.configure(image=self.downloadedThumbnail)
            # Changes the button to now allow downloading.
            self.button.configure(text="Download", command=self.download)
            # Reset the finished label after checking another link.
        except:
            # Error checking if link is invalid.
            self.text.configure("Invalid Link.", text_color="red")

    # Selecting download location.
    def downloadLocation(self):
        self.location = filedialog.askdirectory()

    # Download function defined to download YouTube video.
    def download(self):
        try:
            # We retrieve the highest resolution.
            self.video = self.ytObject.streams.get_highest_resolution()
            self.video.download(self.location)
            self.button.configure(text="Reset application.", command=self.resetButton)
        except:
            self.text.configure("Invalid Link.", text_color="red")

    def resetButton(self):
        # It resets every aspect of the app to default values.
        self.text.configure(text="Insert a youtube video url link.", text_color="white")
        self.thumbnail.configure(image=self.thumbnailImage)
        self.button.configure(text="Select Video", command=self.info)
        self.progressBar.set(0)
        self.link.configure(textvariable="")

    # This is how the progress bar completion gets calculated.
    def on_progress(self, stream, chunk, bytes_remaining):
        # Total size of the video.
        total_size = stream.filesize
        # Number of bytes downloaded.
        bytes_downloaded = total_size - bytes_remaining
        # Decimal point between 0 and 1 that we set to the progressBar variable.
        percentage_of_completion = bytes_downloaded / total_size * 100
        per = round((float(percentage_of_completion) / 100), 2)

        # Updating progress bar
        self.progressBar.set(per)
        self.progressBar.update()

if __name__ == "__main__":
    app = App()
    app.mainloop()