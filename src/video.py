
import threading
import queue
import numpy
import sys
import random
import threading
import av
from av import open
from av.packet import Packet
from av.dictionary import Dictionary
from av import time_base as AV_TIME_BASE
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import time
from videoplay import VideoPlay
from audioplay import AudioPlay

class Video(QThread):
    sigSeconds = pyqtSignal(int)
    def __init__(self, filename, video_queue, audio_queue):
        super(Video,self).__init__()
        self.in_file = filename
        self.video_queue = video_queue
        self.audio_queue = audio_queue
        self.nSeconds = 0

    def run(self):
        video_queue = self.video_queue
        audio_queue = self.audio_queue
        container = open(self.in_file)
        self.nSeconds = container.duration
        print(self.nSeconds)
        self.sigSeconds.emit(self.nSeconds/1000000)
        for packet in container.demux():
            if(packet.dts == None):
                break
            if packet.stream.type == 'video':
                video_queue.put(packet)
            else:
                # continue
                audio_queue.put(packet)
    def reSeconds(self):
        return self.nSeconds


