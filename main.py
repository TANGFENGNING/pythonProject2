from pydub import AudioSegment
import pyaudio
import wave
import numpy as np
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaStreamTrack
import asyncio
from PIL import Image
from io import BytesIO
import base64
import json


# 读取音频文件
def read_audio_file(filename):
    audio = AudioSegment.from_file(filename)
    return audio.raw_data, audio.frame_rate, audio.sample_width


# 播放音频
def play_audio(audio_data, frame_rate, sample_width):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=1,
                    rate=frame_rate,
                    output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()


# 读取图像文件
def read_image_file(filename):
    img = cv2.imread(filename)
    _, buffer = cv2.imencode('.jpg', img)
    img_data = buffer.tostring()
    return img_data


# 显示图像
def show_image(image_data):
    img = Image.open(BytesIO(image_data))
    img.show()


# 发送音频流
async def send_audio(pc, track, audio_data, frame_rate, sample_width):
    while True:
        audio_frame = audio_data[:frame_rate // 10]
        audio_data = audio_data[frame_rate // 10:]
        if len(audio_frame) == 0:
            break
        await track.write(audio_frame)
        await asyncio.sleep(0.1)


# 发送图像流
async def send_image(pc, track, img_data):
    while True:
        await track.write(img_data)
        await asyncio.sleep(0.1)


# 接收音频流
async def receive_audio(pc, track):
    while True:
        audio_frame = await track.recv()
        if not audio_frame:
            break
        play_audio(audio_frame, track.frame_rate, track.sample_width)


# 接收图像流
async def receive_image(pc, track):
    while True:
        img_data = await track.recv()
        if not img_data:
            break
        show_image(img_data)


async def main():
    pc = RTCPeerConnection()

    # 读取音频文件
    audio_data, frame_rate, sample_width = read_audio_file('audio.wav')

    # 创建音频轨道
    audio_track = pc.addTrack(AudioStreamTrack())

    # 读取图像文件
    img_data = read_image_file('image.jpg')

    # 创建图像轨道
    img_track = pc.addTrack(VideoStreamTrack())

    @pc.on('datachannel')
    def on_datachannel(channel):
        @channel.on('message')
        def on_message(message):
            # 收到消息后处理
            print("Received message: ", message)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # 将本地SDP描述发送给对方
    # 对方收到后可以通过RTCPeerConnection.setRemoteDescription()方法设置远程SDP描述
    print("Local SDP: ", pc.localDescription.sdp)

    # 等待对方设置远程SDP描述
    remote_sdp = input("Please enter remote SDP: ")

    # 设置对方的远程SDP描述
    #await pc.setRemoteDescription(RTCSessionDescription(s))
