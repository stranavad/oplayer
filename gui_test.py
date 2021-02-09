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
    
    def initUI(self):
        # PLAYER SIDE
        self.labelPlayer = QtWidgets.QLabel(self)
        self.labelPlayer.setText("Player")
        self.labelPlayer.move(100, 50)

        self.songToPlay = QtWidgets.QComboBox(self)
        self.songToPlay.move(100, 100)
        self.songToPlay.resize(280, 40)
        self.songToPlay.addItem("First choose playlist")

        self.comboPlaylist = QtWidgets.QComboBox(self)
        self.comboPlaylist.move(100, 150)
        self.comboPlaylist.resize(280, 40)
        self.comboPlaylist.currentIndexChanged.connect(self.change_songs)

        self.bPlay = QtWidgets.QPushButton(self)
        self.bPlay.setText("Play")
        self.bPlay.move(100, 200)
        self.bPlay.resize(280, 40)
        self.bPlay.clicked.connect(self.play)

        self.bResume = QtWidgets.QPushButton(self)
        self.bResume.setText("Resume")
        self.bResume.move(100, 250)
        self.bResume.resize(280, 40)
        self.bResume.clicked.connect(self.resume)

        self.bStop = QtWidgets.QPushButton(self)
        self.bStop.setText("Stop")
        self.bStop.move(100, 300)
        self.bStop.resize(280, 40)
        self.bStop.clicked.connect(self.stop)

        # YOUTUBE DOWNLOAD SIDE
        self.labelYoutube = QtWidgets.QLabel(self)
        self.labelYoutube.setText("Youtube downloader")
        self.labelYoutube.move(600, 50)

        self.textboxYoutube = QtWidgets.QLineEdit(self)
        self.textboxYoutube.move(600, 100)
        self.textboxYoutube.resize(280, 40)

        self.comboPlaylistDownload = QtWidgets.QComboBox(self)
        self.comboPlaylistDownload.move(600, 150)
        self.comboPlaylistDownload.resize(280, 40)

        self.textboxYoutubeName = QtWidgets.QLineEdit(self)
        self.textboxYoutubeName.move(600, 200)
        self.textboxYoutubeName.resize(280, 40)

        self.bDownload = QtWidgets.QPushButton(self)
        self.bDownload.setText("Download")
        self.bDownload.move(600, 250)
        self.bDownload.clicked.connect(self.download)

        # CREATE PLAYLIST SIDE
        self.labelCreatePlaylist = QtWidgets.QLabel(self)
        self.labelCreatePlaylist.setText("Create playlist")
        self.labelCreatePlaylist.move(1100, 50)

        self.textboxCreatePlaylist = QtWidgets.QLineEdit(self)
        self.textboxCreatePlaylist.move(1100, 100)
        self.textboxCreatePlaylist.resize(280, 40)

        self.bCreatePlaylist = QtWidgets.QPushButton(self)
        self.bCreatePlaylist.setText("Create Playlist")
        self.bCreatePlaylist.move(1100, 150)
        self.bCreatePlaylist.resize(280, 40)
        self.bCreatePlaylist.clicked.connect(self.create_playlist)

        # VOLUME SLIDER
        self.volumeSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.volumeSlider.move(600, 350)
        self.volumeSlider.resize(280, 40)
        self.volumeSlider.setValue(100)
        self.volumeSlider.valueChanged[int].connect(self.volume_changed)

    def play(self):
        songName, songPath = self.songToPlay.currentText(), self.comboPlaylist.currentText()
        self.player = vlc.MediaPlayer(songPath + "/" + songName + ".mp3")
        self.player.play()
        self.labelPlayer.setText("Playing: " + textboxValue)
        self.update()
    
    def list_folders(self):
        self.comboPlaylistDownload.clear()
        self.comboPlaylist.clear()
        for x in os.listdir('.'):
            if os.path.isdir(x): 
                if x == ".empty":
                    continue
                self.comboPlaylist.addItem(x)
                self.comboPlaylistDownload.addItem(x)

    def change_songs(self):
        self.songToPlay.clear()
        for x in os.listdir(self.comboPlaylist.currentText()):
            if os.path.isfile(self.comboPlaylist.currentText() + "/" + x):
                self.songToPlay.addItem(x.replace(".mp3", ""))

    def create_playlist(self):
        path = self.textboxCreatePlaylist.text()
        try:
            os.mkdir(path)
            self.list_folders()
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
        
        self.list_folders()
    
    def download(self):
        ydl_opts = ydl_opts_mp3
        ydl_opts["outtmpl"] = self.comboPlaylistDownload.currentText() + "/" + self.textboxYoutubeName.text().strip() + ".mp3"
        # ydl_opts = {'outtmpl': 'file_path/file_name'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.textboxYoutube.text()])
    
    def volume_changed(self, value):
        self.player.audio_set_volume(value)
    
    def stop(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)
    
    def update(self):  # Updating the size of elemenrs
        self.labelPlayer.adjustSize()
        self.labelYoutube.adjustSize()

def clicked():
    print("Clicked")


def window():
    app = QApplication([]) # ssys.argv
    win = MyWindow()
    win.update()

    win.show()
    sys.exit(app.exec_())

window()
