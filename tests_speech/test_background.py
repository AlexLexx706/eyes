#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from threading import Thread
from queue import Queue

import speech_recognition as sr
from test_speech_to_text import speak

def recognize_worker(audio_queue, recognizer):
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None:
            break  # stop processing if the main thread is done

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            speak(text)
            print("Google Speech Recognition thinks you said " + text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        audio_queue.task_done()  # mark the audio processing job as completed in the queue

def main():
    # start a new thread to recognize audio, while this thread focuses on listening
    recognizer = sr.Recognizer()
    audio_queue = Queue()

    recognize_thread = Thread(target=recognize_worker, args=(audio_queue, recognizer))
    recognize_thread.daemon = True
    recognize_thread.start()
    while 1:
        with sr.Microphone() as source:
            audio_queue.put(recognizer.listen(source))
            audio_queue.join()

    audio_queue.put(None)  # tell the recognize_thread to stop
    recognize_thread.join()  # wait for the recognize_thread to actually stop

if __name__ == "__main__":
    main()