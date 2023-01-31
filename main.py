# Importing packages needed.
import tkinter as tk
from tkinter import filedialog
import customtkinter
import requests
from pytube import YouTube
from PIL import Image

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
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Thumbnail of link.
        self.thumbnailImage = customtkinter.CTkImage(Image.open("images/thumbnail.png"), size=(192, 144))
        self.thumbnail = customtkinter.CTkLabel(self, text="", image=self.thumbnailImage, bg_color="white")
        self.thumbnail.grid(row=0, column=0, columnspan=2)

        # Text bard on the app.
        self.text = customtkinter.CTkLabel(self, text="Insert a youtube video url link.", bg_color="black")
        self.text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Link input
        self.url_var = tk.StringVar()
        self.link = customtkinter.CTkEntry(self, width=350, height=40, textvariable=self.url_var, bg_color="white")
        self.link.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Main button.
        self.button = customtkinter.CTkButton(self, text="Select Video", command=self.info, height=40, width=250, bg_color="white")
        self.button.grid(row=3, column=0, padx=10)

        # Download location button.
        self.directoryImage = customtkinter.CTkImage(Image.open("images/folder.png"), size=(30, 30))
        self.locationButton = customtkinter.CTkButton(self, text="", image=self.directoryImage, command=self.downloadLocation, height=30, width=40, bg_color="white")
        self.locationButton.grid(row=3, column=1, padx=10)

        # Progress percentage
        self.progressBar = customtkinter.CTkProgressBar(self, height=10, width=500)
        self.progressBar.set(0)
        self.progressBar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Get YouTube video information.
    def info(self):
        try:
            # Calling YouTube information.
            self.ytLink = self.link.get()
            self.ytObject = YouTube(self.ytLink)
            # Changes title to youtube video.
            self.text.configure(text=self.ytObject.title)
            # Changes thumbnail to YouTube video thumbnail.
            self.downloadedThumbnail = customtkinter.CTkImage(Image.open(requests.get(self.ytObject.thumbnail_url, stream=True).raw), size=(192, 144))
            self.thumbnail.configure(image=self.downloadedThumbnail)
            # Changes the button to now allow downloading.
            self.button.configure(text="Download", command=self.download, text_color="white")
            # Reset the finished label after checking another link.
        except:
            # Error checking if link is invalid.
            self.button.configure(text="Invalid Link.", text_color="red")

    # Selecting download location.
    def downloadLocation(self):
        self.location = filedialog.askdirectory()

    # Download function defined to download YouTube video.
    def download(self):
        try:
            self.video = self.ytObject.streams.get_lowest_resolution()
            self.video.download(self.location)
            self.button.configure(text="Download completed.", text_color="green")
        except:
            self.button.configure(text="Invalid Link.", text_color="red")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        per = str(int(percentage_of_completion))

        # Updating progress bar
        self.progressBar.set(float(percentage_of_completion) / 100)

if __name__ == "__main__":
    app = App()
    app.mainloop()