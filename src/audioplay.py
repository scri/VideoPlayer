import ffmpeg
import numpy
import sys
import random
import threading
import av
from av import open
from av.packet import Packet
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import time

class AudioPlay(QThread):
    sigIsPlayTrue = pyqtSignal()
    sigStop = pyqtSignal(bool)
    def __init__(self):
        super(AudioPlay,self).__init__()
        self.in_file = " "
        self.bPlay = True
        self.bStop = False
        self.audioQueue = None
        self.connectSig()


    def connectSig(self):
        self.sigIsPlayTrue.connect(self.playTrue)
        self.sigStop.connect(self.isStop)

    def connectFile(self,filename):
        self.in_file = filename

    def playTrue(self):
        self.bPlay = True
        # self.bStop = False

    def setQueue(self, qQueue):
        self.audioQueue = qQueue

    def isStop(self, bStop):
        self.bStop = bStop

    def run(self):
        print("run auydio")
        audioQueue = self.audioQueue
        qformat = QAudioFormat()
        qformat.setByteOrder(QAudioFormat.LittleEndian)
        qformat.setChannelCount(2)
        qformat.setCodec('audio/pcm')
        qformat.setSampleRate(48000)
        qformat.setSampleSize(16)
        qformat.setSampleType(QAudioFormat.SignedInt)
        print("run auydio")
        resampler = av.AudioResampler(
            format=av.AudioFormat('s16').packed,
            layout='stereo',
            rate=48000,
        )
        output = QAudioOutput(qformat)
        output.setBufferSize(2 * 2 * 48000)
        device = output.start()
        while(1):
            if(self.bPlay == True and self.bStop == False):
                if not audioQueue.empty():
                    audioPacket = audioQueue.get()
                else:
                    time.sleep(0.030)
                    continue
                if (audioPacket.dts == None):
                    return

                for frame in audioPacket.decode():
                    # some other formats gray16be, bgr24, rgb24
                    # buffering_nums = buffer_time_in_ms / delta_in_ms
                    frame.pts = None
                    frame = resampler.resample(frame)
                    bytes_buffered = output.bufferSize() - output.bytesFree()
                    us_processed = output.processedUSecs()
                    us_buffered = 1000000 * bytes_buffered / (2 * 16 / 8) / 48000
                    data = frame.planes[0].to_bytes()
                    while data and self.bStop == False:
                        written = device.write(data)
                        if written:
                            data = data[written:]
                        else:
                            time.sleep(0.033)
if __name__ == '__main__':
    file_path = 'C:/Users/Public/Videos/Sample Videos/动物.wmv'
    out = AudioPlay()
    out.connectFile(file_path)
    out.run()