import pvporcupine
import sounddevice as sd
import struct
import numpy as np
import whisper
from llm_agent import generate_prompt, get_response, classify_intent_with_llm
import subprocess
import queue
import os
import pvporcupine
from dialog_manager import DialogManager



# Load models
whisper_model = whisper.load_model("base")

# Wake word engine
access_key = "N8PyxcgsBjc2ve8aX7od/60wZ6uyhG7SwRAJi7NPeLviSZiDtqv3QQ=="
porcupine = pvporcupine.create(
    access_key=access_key,
    keywords=["jarvis"]
)
q = queue.Queue()

# macOS TTS function
def speak(text):
    subprocess.run(["say", text])

# Main LLM handler
def ask_llm_and_speak(user_input):
    print(f"You said: {user_input}")
    prompt = generate_prompt({}, user_input)
    intent = classify_intent_with_llm(user_input)
    print(f"Intent: {intent}")
    prompt = generate_prompt({}, user_input)
    reply = get_response(prompt)
    print(f"Bot: {reply}")
    speak(reply)
    return reply


# Wait for wake word
def detect_wake_word():
    print("Say 'jarvis' to begin...")

    def audio_callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=porcupine.sample_rate, blocksize=porcupine.frame_length,
                           dtype='int16', channels=1, callback=audio_callback):
        while True:
            pcm = q.get()
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected!")
                return

#  Record speech after wake word
def capture_text():
    print("Listening for speech...")

    # Record 5 seconds of audio
    audio_data = sd.rec(int(10 * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()

    print("Transcribing...")
    result = whisper_model.transcribe(np.squeeze(audio_data), fp16=False)
    user_text = result["text"].strip()

    if user_text:
        return user_text
    return ""
