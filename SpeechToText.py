# Continuous Speech to Text Conversion with Web UI
# Author: Manish Choudhari
# Prerequisites: Install SpeechRecognition library using        pip install SpeechRecognition
# pip install gradio SpeechRecognition pyaudio    

import gradio as gr
import speech_recognition as sr
import threading
import time

recognizer = sr.Recognizer()
mic = sr.Microphone()

is_listening = False
full_text = ""
lock = threading.Lock()

# MIC LISTENER

def listen_loop():
    global is_listening, full_text

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        if not is_listening:
            time.sleep(0.1)
            continue

        try:
            with mic as source:
                audio = recognizer.listen(
                    source,
                    timeout=1,
                    phrase_time_limit=5
                )

            # Prevent extra sentence after pause
            if not is_listening:
                continue

            text = recognizer.recognize_google(audio)

            with lock:
                full_text += text + "\n"
                with open("output.txt", "w") as f:
                    f.write(full_text)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            with lock:
                full_text += f"[API Error: {e}]\n"

# AUDIO FILE UPLOAD

def transcribe_audio_file(audio_file):
    global full_text

    if audio_file is None:
        return full_text

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        with lock:
            full_text += text + "\n"
            with open("output.txt", "w") as f:
                f.write(full_text)

    except sr.UnknownValueError:
        full_text += "[Could not understand audio]\n"
    except sr.RequestError as e:
        full_text += f"[API Error: {e}]\n"

    return full_text

# BUTTON EVENTS HANDLERS

def start_listening():
    global is_listening
    is_listening = True
    return (
        full_text,
        gr.update(interactive=False),  # Disable Speak
        gr.update(interactive=True)    # Enable Pause
    )

def pause_listening():
    global is_listening
    is_listening = False
    return (
        full_text,
        gr.update(interactive=True),   # Enable Speak
        gr.update(interactive=False)   # Disable Pause
    )

def clear_text():
    global full_text
    with lock:
        full_text = ""
        with open("output.txt", "w") as f:
            f.write("")
    return full_text

def get_text():
    return full_text

# Start background listener thread
threading.Thread(target=listen_loop, daemon=True).start()

# UI LAYOUT

with gr.Blocks(title="Speech to Text App") as demo:
    gr.Markdown("## Continuous Speech to Text")
    gr.Markdown("Live microphone or upload an audio file. Pause anytime.")

    with gr.Row():
        # LEFT PANEL
        with gr.Column(scale=1):
            speak_btn = gr.Button("Speak Now", interactive=True)
            pause_btn = gr.Button("Pause", interactive=False)
            clear_btn = gr.Button("Clear Text")

            gr.Markdown("### Upload Audio")
            audio_input = gr.Audio(
                type="filepath",
                label="Upload WAV / MP3 audio file"
            )

        # RIGHT PANEL
        with gr.Column(scale=3):
            output_text = gr.Textbox(
                label="Generated Text",
                lines=20,
                max_lines=None,
                autoscroll=True
            )

    # EVENTS

    speak_btn.click(
        start_listening,
        outputs=[output_text, speak_btn, pause_btn]
    )

    pause_btn.click(
        pause_listening,
        outputs=[output_text, speak_btn, pause_btn]
    )

    clear_btn.click(
        clear_text,
        outputs=output_text
    )

    audio_input.change(
        fn=transcribe_audio_file,
        inputs=audio_input,
        outputs=output_text
    )

    gr.Timer(1).tick(fn=get_text, outputs=output_text)

demo.launch()
