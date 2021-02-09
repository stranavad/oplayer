from __future__ import unicode_literals
import tkinter as tk
import youtube_dl

mainframe = ""
root = ""
ydl_opts_mp4 = {
    "format" : "best",
}

ydl_opts_mp3 = {
    "format" : "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    }], 
}

def download_mp3(link):
    mainframe.destroy()
    with youtube_dl.YoutubeDL(ydl_opts_mp3) as ydl:
        ydl.download([link])
    downloaded_screen()

def download_mp4(link):
    global mainframe
    global root
    mainframe.destroy()
    with youtube_dl.YoutubeDL(ydl_opts_mp4) as ydl:
        ydl.download([link])
    downloaded_screen()

def waiting_screen():
    global mainframe
    global root
    root.title("Wating")
    mainframe = tk.Frame(root)
    mainframe.place(relwidth=1, relheight=1)

    heading = tk.Label(mainframe, text="Downloading...", font=("Courier", 16))
    heading.place(relwidth=0.4, relx=0.3, rely=0, relheight=0.1)

    root.mainloop()

def downloaded_screen():
    global mainframe
    global root
    root.title("Downloaded!")
    mainframe = tk.Frame(root)
    mainframe.place(relwidth=1, relheight=1)

    heading = tk.Label(mainframe, text="Downloaded!", font=("Courier", 16))
    heading.place(relwidth=0.4, relheight=0.1,
                       relx=0.3, rely=0)

    again_button = tk.Button(mainframe, text="Download again", padx=10,
                          pady=5, font=("Courier", 14), bg="white",
                          command=lambda: [mainframe.destroy(), Home(True)])
    again_button.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.2)

    close_button = tk.Button(mainframe, text="Exit", padx=10,
                          pady=5, font=("Courier", 14), bg="white",
                          command=lambda: root.destroy())
    close_button.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.35)

    root.mainloop()


def Home(exists):
    global mainframe
    global root
    if not exists:
        root = tk.Tk()
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack()
    root.title("Youtube downloader")
    mainframe = tk.Frame(root)
    mainframe.place(relwidth=1, relheight=1)

    linkText = tk.Label(mainframe, text="Link: ", font=("Courier", 14))
    linkText.place(relwidth=0.3, relheight=0.07,
                       relx=0, rely=0.1)
    link_entry = tk.Entry(mainframe, bg="white", font=("Courier", 12))
    link_entry.place(relwidth=0.6, relheight=0.07, relx=0.35, rely=0.1)

    mp3Button = tk.Button(mainframe, text="Mp3 download", padx=10,
                          pady=5, font=("Courier", 14), bg="white",
                          command=lambda: download_mp3(link_entry.get()))
    mp3Button.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.3)

    mp4Button = tk.Button(mainframe, text="Mp4 download", padx=10,
                          pady=5, font=("Courier", 14), bg="white",
                          command=lambda: download_mp4(link_entry.get()))
    mp4Button.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.45)

    root.mainloop()

Home(False)