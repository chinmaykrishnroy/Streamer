from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QListWidget, QSlider, QLabel, QComboBox, QMainWindow)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QPoint, QTimer
import sys
from youtubesearchpython import VideosSearch
import yt_dlp
import os
import tempfile
from datetime import datetime

styles = """
/* style.css */

/* General Styles */
QWidget {
    background-color: transparent;
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #F1FAEE;
}

QListWidget {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #222222, stop: 1 #444444);
    border: 1px solid #222222;
    border-radius: 5px;
    padding: 0px;
    color: #F1FAEE;
    font-size: 14px;
}

QComboBox {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #380036, stop:1 #0CBABA);
    border: 1px solid #222222;
    border-radius: 5px;
    padding: 0px;
    color: #F1FAEE;
    font-size: 14px;
}

QLineEdit {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #222222, stop: 1 #444444);
    border: 1px solid #222222;
    border-radius: 5px;
    padding-bottom: 4px;
    padding-left: 12px;
    color: #F1FAEE;
    font-size: 24px;
}

QPushButton#closeButton {
    background-color: #fb4c24;
    color: #F1FAEE;
    border: 1px solid #222222;
    padding: 10px;
    border-radius: 5px;
    font-size: 20px;
    padding: 0px 8px;
    padding-left: 13px;
    padding-right: 13px;
    padding-bottom: 6px;
    font-family: 'Segoe UI', sans-serif;
    border-radius: 16px;
}

QPushButton#closeButton:hover {
    background-color: #4d4d4d;
}

QPushButton#closeButton:pressed {
    background-color: #030301;
}


QLineEdit:focus,
QListWidget:focus,
QComboBox:focus {
    background-color: #003b45;
    color: #F1FAEE;
}

QPushButton {
    background-color: #080932;
    color: #F1FAEE;
    border: none;
    border-radius: 5px;
    padding: 7px 12px;
    font-size: 18px;
}

QPushButton:hover {
    background-color: #fb4c24;
    color: #F1FAEE;
}

QPushButton:pressed {
    background-color: #d4d4d4;
    color: #000000;
}


QSlider::groove:horizontal {
    border: 0px solid #535353;
    height: 6px;
    background: #4d4d4d;
    margin: 0px 0;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #464646;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #fb4c24;
}

QSlider::sub-page:horizontal {
    background: #fb4c24;
    border: 1px solid #fb4c24;
    height: 6px;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #4d4d4d;
    border: 1px solid #4d4d4d;
    height: 6px;
    border-radius: 3px;
}

QScrollBar:horizontal {
    border: none;
    background: #ffffff;
    height: 4px;
    margin: 0px 20px 0 20px;
}

QScrollBar::handle:horizontal {
    background: #50425b;
    min-width: 20px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background: #fb4c24;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    background: none;
}

QScrollBar:vertical {
    border: none;
    background: #ffffff;
    width: 4px;
    margin: 20px 0 20px 0;
}

QScrollBar::handle:vertical {
    background: #50425b;
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #fb4c24;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none;
}

QLabel {
    color: #F1FAEE;
}

QMainWindow {
    background-color: #030301;
}

QVideoWidget {
    border: 2px solid #fb4c24;
    border-radius: 10px;
}

QListWidget {
    background-color: #030301;
    border: none;
    color: #F1FAEE;
    font-size: 14px;
}

QListWidget {
    background-color: #030301;
    border: none;
    color: #F1FAEE;
    font-size: 14px;
}

QListWidget::item {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #004256, stop: 1 #20233e);
    margin: 5px;
    /* Space between items */
    padding: 10px;
    border-radius: 5px;
}

QListWidget::item:hover {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #aa0033, stop: 1 #910c00);
}

QListWidget::item:selected {
    background-color: #4d4d4d;
    color: #F1FAEE;
}
"""

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.video_widget = QVideoWidget()
        self.setCentralWidget(self.video_widget)
        self.is_fullscreen = False
        self.video_widget.mouseDoubleClickEvent = self.toggle_fullscreen
        self.offset = None

    def toggle_fullscreen(self, event):
        if self.is_fullscreen:
            self.showNormal()
            self.unsetCursor()
        else:
            self.showFullScreen()
            self.setCursor(Qt.BlankCursor)            
        self.is_fullscreen = not self.is_fullscreen

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

class SeekSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            value = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
            self.setValue(int(value))
            self.sliderMoved.emit(int(value))
        super().mousePressEvent(event)

class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.temp_dir = ""
        self.setWindowTitle("YouTube Player")
        self.setGeometry(100, 100, 640, 360)

        # Layouts
        layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        controls_layout = QHBoxLayout()

        # Search bar and button
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_video)

        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        # Video list
        self.video_list = QListWidget()
        self.video_list.itemClicked.connect(self.download_and_play_video)

        # Video player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video seek slider
        self.seek_slider = SeekSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 100)
        self.seek_slider.sliderMoved.connect(self.seek_video)

        # Controls
        self.play_button = QPushButton("Play ")
        self.pause_button = QPushButton("Pause")
        self.seek_back_button = QPushButton("< 10s")
        self.seek_forward_button = QPushButton("10s >")
        self.close_button = QPushButton("x")
        self.close_button.setObjectName("closeButton")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)
        self.media_player.setVolume(75)
        self.playback_speed = QComboBox()
        self.playback_speed.addItems(["0.5", "0.75x", "1x", "1.5x", "2x"])
        self.playback_speed.setCurrentIndex(2)

        self.play_button.clicked.connect(self.handle_play)
        self.pause_button.clicked.connect(self.handle_pause)
        self.seek_back_button.clicked.connect(lambda: self.media_player.setPosition(self.media_player.position() - 10000))
        self.seek_forward_button.clicked.connect(lambda: self.media_player.setPosition(self.media_player.position() + 10000))
        self.volume_slider.valueChanged.connect(self.media_player.setVolume)
        self.playback_speed.currentIndexChanged.connect(self.set_playback_speed)
        self.close_button.clicked.connect(self.close_app)

        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.seek_back_button)
        controls_layout.addWidget(self.seek_forward_button)
        controls_layout.addWidget(QLabel("Volume"))
        controls_layout.addWidget(self.volume_slider)
        controls_layout.addWidget(QLabel("Speed"))
        controls_layout.addWidget(self.playback_speed)
        controls_layout.addWidget(self.close_button)

        # Add widgets to the layout
        layout.addLayout(search_layout)
        layout.addWidget(self.video_list)
        layout.addWidget(self.seek_slider)  # Add the seek slider to the layout
        layout.addLayout(controls_layout)

        self.setLayout(layout)

        self.video_window = VideoWindow()
        self.media_player.setVideoOutput(self.video_window.video_widget)
        self.current_video_path = None

        # Connect the app quit signal to clean up files
        app.aboutToQuit.connect(self.cleanup_temp_files)

        # Timer to update the seek slider
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # Update every second
        self.timer.timeout.connect(self.update_seek_slider)
        self.timer.start()

        self.is_fullscreen = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def handle_pause(self):
        self.media_player.pause()
        self.video_window.hide()

    def handle_play(self):
        self.media_player.play()
        self.video_window.show()

    def close_app(self):
        self.cleanup_temp_files()  # Ensure temp files are cleaned up
        self.video_window.close()  # Close the video window
        self.close()  # Close the main window
        QApplication.instance().quit()  # Quit the application

    def search_video(self):
        search_query = self.search_bar.text()
        videos_search = VideosSearch(search_query, limit=10)
        results = videos_search.result()

        self.video_list.clear()
        for video in results['result']:
            self.video_list.addItem(f"{video['title']} - {video['link']}")

    def download_and_play_video(self, item):
        video_url = item.text().split(' - ')[-1]
        self.temp_dir = tempfile.gettempdir()
        self.current_video_path = os.path.join(tempfile.gettempdir(), f'PyStreamer{datetime.now().strftime("%Y%m%d%H%M%S")}.mp4')
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'merge_output_format': 'mp4',
            'outtmpl': self.current_video_path,
            'quiet': True,
            'ffmpeg_location': 'C:/ffmpeg/bin',
        }
        self.cleanup_temp_files()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

        self.video_list.clear()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.current_video_path)))
        self.video_list.addItem("File is Ready!")
        print(self.current_video_path)
        self.open_video_window()

    def open_video_window(self):
        self.video_window.show()
        self.media_player.play()

    def set_playback_speed(self):
        speed = float(self.playback_speed.currentText().replace('x', ''))
        self.media_player.setPlaybackRate(speed)

    def seek_video(self, position):
        self.media_player.setPosition(int(self.media_player.duration() * position / 100))

    def update_seek_slider(self):
        if self.media_player.duration() > 0:
            self.seek_slider.setValue(int(self.media_player.position() * 100 / self.media_player.duration()))

    def cleanup_temp_files(self):
        if os.path.exists(tempfile.gettempdir()):
            for file in os.listdir(tempfile.gettempdir()):
                if file.startswith('PyStreamer'):
                    try:
                        os.remove(os.path.join(tempfile.gettempdir(), file))
                        print("Removed File: ", file)
                    except Exception as e:
                        print(f"Error while deleting file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(styles)
    player = YouTubePlayer()
    player.show()
    sys.exit(app.exec_())
