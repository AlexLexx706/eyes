from gtts import gTTS
from io import BytesIO
import pyaudio
import pydub
import wave
import time


def speak(phrase, max_time=1):
    tts = gTTS(phrase, lang='ru')
    tts.save('hello.mp3')

    sound = pydub.AudioSegment.from_mp3("hello.mp3")
    sound.export("hello.wav", format="wav")

    wav_file = wave.open("hello.wav", 'rb')

    chunk_size = 1024
    # Instantiate PyAudio.
    port_audio = pyaudio.PyAudio()

    # Open stream.
    stream = port_audio.open(
        format=port_audio.get_format_from_width(wav_file.getsampwidth()),
        channels=wav_file.getnchannels(),
        rate=wav_file.getframerate(),
        output=True)

    data = wav_file.readframes(chunk_size)
    while len(data):
        stream.write(data)
        data = wav_file.readframes(chunk_size)
    wav_file.rewind()

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    port_audio.terminate()

if __name__ == '__main__':
    speak('как дела')