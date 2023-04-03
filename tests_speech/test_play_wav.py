'''
Module to play WAV files using PyAudio.
Author: Vasudev Ram - http://jugad2.blogspot.com
Adapted from the example at:
https://people.csail.mit.edu/hubert/pyaudio/#docs
PyAudio Example: Play a wave file.
'''

import pyaudio
import wave
import sys
import os.path
import time

CHUNK_SIZE = 1024

def play_wav(wav_filename, chunk_size=CHUNK_SIZE):
    # open wav file
    wav_file = wave.open(wav_filename, 'rb')

    # Instantiate PyAudio.
    port_audio = pyaudio.PyAudio()

    # Open stream.
    stream = port_audio.open(
        format=port_audio.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True)

    count = 0
    # play soun 10 times
    while count < 10:
        data = wav_file.readframes(chunk_size)
        while len(data):
            stream.write(data)
            data = wav_file.readframes(chunk_size)
        wav_file.rewind()
        time.sleep(1)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    port_audio.terminate()

def main():
    for wav_filename in ['./sounds/hi_agniia.wav', ]:
        # Remove trailing newline.
        play_wav(wav_filename)
        time.sleep(3)

if __name__ == '__main__':
    main()