
import numpy
import sys
import random
import threading
import av
from av import open
from av.packet import Packet
from av import time_base as AV_TIME_BASE

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import time
# from PyQt5 import Q

class VideoPlay(QThread):
    sigGetOneFrame  = pyqtSignal(QImage)
    sigIsPlayTrue = pyqtSignal()
    sigStop = pyqtSignal(bool)
    sigSeconds = pyqtSignal(int)
    def __init__(self):
        super(VideoPlay,self).__init__()
        self.bPlay = True
        self.bStop = False
        self.videoQueue = None
        self.connectSig()
    def connectSig(self):
        self.sigIsPlayTrue.connect(self.playTrue)
        self.sigStop.connect(self.isStop)

    def connectFile(self,filename):
        self.in_file = filename

    def playTrue(self):
        self.bPlay = True

    def setQueue(self, qQueue):
        self.videoQueue = qQueue

    def isStop(self, bStop):
        self.bStop = bStop

    def run(self):
        videoQueue = self.videoQueue
        last_pts = 0
        pts_delta = 0
        last_show_time = 0
        sleep_time = 0
        while(1):
            if(self.bPlay == True and self.bStop == False):
                if not videoQueue.empty():
                    videoPacket = videoQueue.get()
                else:
                    time.sleep(0.0001)
                    continue
                if (videoPacket.dts == None):
                    return
                sleep_time = 0
                for frame in videoPacket.decode():
                    # some other formats gray16be, bgr24, rgb24
                    img2 = frame.to_ndarray(format='rgb24')
                    image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                     QtGui.QImage.Format_RGB888)

                    pts_delta = frame.pts - last_pts
                    pts_delta = pts_delta / 100000.0
                    show_time = time.time()
                    if show_time < last_show_time + pts_delta - 0.001:
                        sleep_time = last_show_time + pts_delta - show_time - 0.001
                        print(sleep_time)
                        time.sleep(sleep_time)
                    self.bPlay = False
                    self.sigGetOneFrame.emit(image)
                    self.sigSeconds.emit(frame.pts)
                    last_pts = frame.pts
                    last_show_time = time.time()

def timestamp_to_frame(timestamp, stream):
    fps = stream.rate
    time_base = stream.time_base
    start_time = stream.start_time
    frame = (timestamp - start_time ) * float(time_base) / float(fps)
    return frame

def read_frame_as_jpeg(in_file, frame_num):
    """
    指定帧数读取任意帧
    """
    container = open(in_file)
    print(container.duration)
    # print(container.rate)
    # container = av.open(fate_suite('h264/interlaced_crop.mp4'))

    video_stream = next(s for s in container.streams if s.type == 'video')

    audio_stream = container.streams.audio[0]

    qformat = QAudioFormat()
    qformat.setByteOrder(QAudioFormat.LittleEndian)
    qformat.setChannelCount(2)
    qformat.setCodec('audio/pcm')
    qformat.setSampleRate(48000)
    qformat.setSampleSize(16)
    qformat.setSampleType(QAudioFormat.SignedInt)

    resampler = av.AudioResampler(
        format=av.AudioFormat('s16').packed,
        layout='stereo',
        rate=48000,
    )

    output = QAudioOutput(qformat)
    output.setBufferSize(2 * 5 * 48000)
    device = output.start()
    # total_frame_count = 0
    #
    # # Count number of frames in video
    # for packet in container.demux(video_stream):
    #     #for frame in packet.decode():
    #     total_frame_count += 1
    #
    # target_frame = int(total_frame_count / 2.0)
    # time_base = float(video_stream.time_base)
    #
    # rate = float(video_stream.average_rate)
    # target_sec = target_frame * 1 / rate
    #
    # target_timestamp = int(target_sec / time_base) + video_stream.start_time
    # print(target_timestamp)
    # # video_stream.seek(target_timestamp)
    #
    # current_frame = None
    # frame_count = 0
    pts = 0
    # ii = 0
    while(1):
    # for packet in container.demux(video_stream):
        packet = next(container.demux())
        # if (packet.dts == None):
        #     break
        print(packet.dts)
        if packet is not None:
            for frame in packet.decode():
                index = frame.index
                if packet.stream.type == 'video':
                    print(frame)
                    # packet = output_v.encode(frame)
                else:
                    print(frame)
                    # packet.stream = output_a
        for frame in packet.decode():
            index = frame.index
            if packet.stream.name == 'pcm_alaw' or packet.stream.name == 'pcm_ulaw':
                pts_delta = 160
                delta_in_ms = pts_delta / 8
            else:
                pts_delta = frame.samples * 90000 / frame.rate
                delta_in_ms = pts_delta * 1000 / frame.rate
            #buffering_nums = buffer_time_in_ms / delta_in_ms
            print(frame.pts)
            frame.pts = None
            pts += 1
            frame = resampler.resample(frame)
            print(pts)
            print(output.state())
            print(frame)
            bytes_buffered = output.bufferSize() - output.bytesFree()
            us_processed = output.processedUSecs()
            us_buffered = 1000000 * bytes_buffered / (2 * 16 / 8) / 48000
            # player = QMediaPlayer()
            # frame.
            # player.setMedia(frame.planes[0].to_bytes())
            # player.play()
            data = frame.planes[0].to_bytes()
            while data:
                written = device.write(data)
                if written:
                    # print 'wrote', written
                    data = data[written:]
                else:
                    # print 'did not accept data; sleeping'
                    time.sleep(0.033)
        #     if packet.stream.type == 'video':
        #         print(packet.stream.type)
        #     else:
        #         print(packet.stream.type)

    #     for frame in packet.decode():
    #         img = frame.to_nd_array(format='bgr24')
    #         cv2.imshow("Test", img)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #         if current_frame is None:
    #             current_frame = timestamp_to_frame(frame.pts, video_stream)
    #
    #         else:
    #             current_frame += 1
    #     # start counting once we reach the target frame
    #         if current_frame is not None and current_frame >= target_frame:
    #             frame_count += 1
    #         if(frame_count == 10):
    #             video_stream.seek(target_timestamp)
    # # self.assertEqual(frame_count, total_frame_count - target_frame)
    # print(current_frame)
    # print(frame_count)
    # print(total_frame_count)
    # print(frame_count == (total_frame_count - target_frame))
    # cv2.destroyAllWindows()
    print(pts)



if __name__ == '__main__':
    file_path = 'C:/Users/Public/Videos/Sample Videos/动物.wmv'
    out = read_frame_as_jpeg(file_path, 900)
    image_array = numpy.asarray(bytearray(out), dtype="uint8")
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    cv2.imshow('frame', image)
    cv2.waitKey()

