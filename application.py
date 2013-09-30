#!/usr/bin/env python3

# Python Multimedia Streaming
# corpg - September 2013
# Licensed under GPLv2

# To enable OSS emulation with alsa, load the following modules:
#   - snd-mixer-oss
#   - snd-seq-oss
#   - snd-pcm-oss

import ossaudiodev, wave
import socket

# 3 sec buffer
BUFFER=2048
AUDIO_DEVICE=/dev/dsp
PORT=9000
SERVER_IP=192.168.0.100

def client(file):
    # open the audio file
    f = wave.open(file, "r")
    
    # connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    
    # Start streaming
    print("Start streaming music...")
    try:
        while 1:
            d = f.readframes(BUFFER)
            if d:
                s.send(d)
            else:
                break
    finally:
        f.close()


# The server is only compatible with Linux
def server():
    # audio device intialization
    dev=ossaudiodev.open(AUDIO_DEVICE,"w")
    # hardcoded parameters - should be received by the client
    dev.setparameters(ossaudiodev.AFMT_S16_LE, 2, 44100)
    
    # start the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    print("Server is listening...")
    
    # Play music !
    while 1:
        c, _ = s.accept()
        print("New connection. Start playing music...")
        dev.write(c.recv(BUFFER)))

