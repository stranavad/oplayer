from __future__ import unicode_literals
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
import vlc
import sys
import os
import youtube_dl

ydl_opts_mp3 = {
    "format" : "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    }],
}

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 1500, 500)
        self.setWindowTitle("oPlayer")
        self.initUI()
        self.player = vlc.MediaPlayer()
        self.folders = self.list_folders()

    # Main UI
    def initUI(self):
        # PLAYER SIDE
        self.create_play_part()

        # YOUTUBE DOWNLOAD SIDE
        self.create_download_part()

        # CREATE PLAYLIST SIDE
        self.create_playlist_part()

        # VOLUME SLIDER
        self.create_app_controls()

    # UI PARTS
    def create_play_part(self):
        self.label_player = QtWidgets.QLabel(self)
        self.label_player.setText("Player")
        self.label_player.move(100, 50)

        self.song_to_play = QtWidgets.QComboBox(self)
        self.song_to_play.move(100, 100)
        self.song_to_play.resize(280, 40)
        self.song_to_play.addItem("First choose playlist")

        self.combo_playlist = QtWidgets.QComboBox(self)
        self.combo_playlist.move(100, 150)
        self.combo_playlist.resize(280, 40)
        self.combo_playlist.currentIndexChanged.connect(self.change_songs)

        self.button_play = QtWidgets.QPushButton(self)
        self.button_play.setText("Play")
        self.button_play.move(100, 200)
        self.button_play.resize(280, 40)
        self.button_play.clicked.connect(self.play)

        self.button_resume = QtWidgets.QPushButton(self)
        self.button_resume.setText("Resume")
        self.button_resume.move(100, 250)
        self.button_resume.resize(280, 40)
        self.button_resume.clicked.connect(self.resume)

        self.button_stop = QtWidgets.QPushButton(self)
        self.button_stop.setText("Stop")
        self.button_stop.move(100, 300)
        self.button_stop.resize(280, 40)
        self.button_stop.clicked.connect(self.stop)

    def create_download_part(self):
        self.label_youtube = QtWidgets.QLabel(self)
        self.label_youtube.setText("Youtube downloader")
        self.label_youtube.move(600, 50)

        self.textbox_youtube = QtWidgets.QLineEdit(self)
        self.textbox_youtube.move(600, 100)
        self.textbox_youtube.resize(280, 40)

        self.combo_playlist_download = QtWidgets.QComboBox(self)
        self.combo_playlist_download.move(600, 150)
        self.combo_playlist_download.resize(280, 40)

        self.textbox_youtube_name = QtWidgets.QLineEdit(self)
        self.textbox_youtube_name.move(600, 200)
        self.textbox_youtube_name.resize(280, 40)

        self.button_download = QtWidgets.QPushButton(self)
        self.button_download.setText("Download")
        self.button_download.move(600, 250)
        self.button_download.clicked.connect(self.download)

    def create_playlist_part(self):
        self.label_create_playlist = QtWidgets.QLabel(self)
        self.label_create_playlist.setText("Create playlist")
        self.label_create_playlist.move(1100, 50)

        self.textbox_create_playlist = QtWidgets.QLineEdit(self)
        self.textbox_create_playlist.move(1100, 100)
        self.textbox_create_playlist.resize(280, 40)

        self.button_create_playlist = QtWidgets.QPushButton(self)
        self.button_create_playlist.setText("Create Playlist")
        self.button_create_playlist.move(1100, 150)
        self.button_create_playlist.resize(280, 40)
        self.button_create_playlist.clicked.connect(self.create_playlist)

    def create_app_controls(self):
        self.volume_slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.volume_slider.move(600, 350)
        self.volume_slider.resize(280, 40)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged[int].connect(self.volume_changed)

    # Music controls
    def play(self):
        self.player.set_pause(1)
        songName, songPath = self.song_to_play.currentText(), self.combo_playlist.currentText()
        self.player = vlc.MediaPlayer(songPath + "/" + songName + ".mp3")
        self.player.play()
        self.label_player.setText("Playing: " + songName)
        self.update()

    def volume_changed(self, value):
        self.player.audio_set_volume(value)

    def stop(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)

    # Youtube download
    def download(self):
        ydl_opts = ydl_opts_mp3
        ydl_opts["outtmpl"] = self.combo_playlist_download.currentText() + "/" + self.textbox_youtube_name.text().strip() + ".mp3"
        # ydl_opts = {'outtmpl': 'file_path/file_name'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.textbox_youtube.text()])

    # Creating playlists-folders
    def create_playlist(self):
        path = self.textbox_create_playlist.text()
        print(path)
        try:
            os.mkdir(path)
            # self.list_folders()
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        self.list_folders()

    # Updating UI elements
    def update(self):  # Updating the size of elements
        self.label_player.adjustSize()
        self.label_youtube.adjustSize()

    def list_folders(self):  # Changing folders in dropdowns
        self.combo_playlist_download.clear()
        self.combo_playlist.clear()
        for x in os.listdir('.'):
            if os.path.isdir(x):
                if x == ".empty" or x == ".git":
                    continue
                self.combo_playlist.addItem(x)
                self.combo_playlist_download.addItem(x)

    def change_songs(self):  # Changing songs in dropdown based on the playlist choosed
        self.song_to_play.clear()
        if self.combo_playlist.currentText() != "":
            for x in os.listdir(self.combo_playlist.currentText()):
                if os.path.isfile(self.combo_playlist.currentText() + "/" + x):
                    self.song_to_play.addItem(x.replace(".mp3", ""))


# The init function
def window():
    app = QApplication([]) # ssys.argv
    win = MyWindow()
    win.update()

    win.show()
    sys.exit(app.exec_())

window()
