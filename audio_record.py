import pyaudio
import wave
import numpy as np
import time
import keyboard
import json
import subprocess

# Open the JSON file and load settings
with open('settings.config', 'r') as file:
    setting = json.load(file)

RECORD_SECONDS = setting["RECORD_SECONDS"]              # in seconds
QUITE_THRESHOLD = setting["QUITE_THRESHOLD"]            # in seconds
WAVE_OUTPUT_FILENAME = setting["WAVE_OUTPUT_FILENAME"]
THRESHOLD = setting["THRESHOLD"]                        # recording threshold  (0 min, 1 max)
HOTKEY_NAME = setting["HOTKEY_FOR_TERMINATION"]         # hotkey name in keyboard module
PATH_TO_RAW = setting["path_to_so-vits_raw"]

# Define the loop variables
RUNNING = True
# COUNTING = 1

# Define the audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Callback function for key pressing
def on_hotkey_press():
    global RUNNING
    RUNNING = False

# White audio file
def write_audio_file(file_name, audio_frames, audio_instance):
    # Save the recorded audio as a .wav file
    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio_instance.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(audio_frames))
    wave_file.close()

if __name__ == "__main__":
    # Register the Page Down key press event
    keyboard.add_hotkey(HOTKEY_NAME, on_hotkey_press)

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    # Start recording when the volume exceeds the threshold
    recording = False
    frames = []
    start_time = time.time()
    last_audio_time = time.time()
    SAVE_FILE = False

    while RUNNING:
        data = stream.read(CHUNK)
        # Convert the audio data to a numpy array of floats
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        # Normalize the audio data to a maximum amplitude of 1.0
        audio_data /= 32768.0
        # Compute the root mean square (RMS) value of the audio data
        rms = np.sqrt(np.mean(np.square(audio_data)))
        if rms >= THRESHOLD:
            # Start recording if not already recording
            if not recording:
                print("Recording started")
                recording = True
            frames.append(data)
            last_audio_time = time.time()
        else:
            # Stop recording if currently recording and there has been a pause longer than 1.5 seconds
            if recording and time.time() - last_audio_time >= QUITE_THRESHOLD:
                print("Recording stopped due to pause")
                SAVE_FILE = True
                recording = False
            else:
                if recording:
                    frames.append(data)

        # Check if it's time to save the audio file
        elapsed_time = time.time() - start_time
        if elapsed_time >= RECORD_SECONDS:
            SAVE_FILE = True

        # Stop recording if currently recording and the maximum recording duration has been reached
        if recording and time.time() - last_audio_time > RECORD_SECONDS:
            print("Recording stopped due to maximum duration or paused too long")
            SAVE_FILE = True
            recording = False

        if SAVE_FILE:
            # name = PATH_TO_RAW + WAVE_OUTPUT_FILENAME + str(COUNTING) + ".wav"          # debug purpose
            name = PATH_TO_RAW + WAVE_OUTPUT_FILENAME + ".wav"
            write_audio_file(name, frames, audio)
            frames = []
            start_time = time.time()
            SAVE_FILE = False

            # call to push
            process = subprocess.Popen(["python", "output_to_mic.py"], shell=True)

            # o2m.send2Change()



    # Stop and close the microphone stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Process terminated")