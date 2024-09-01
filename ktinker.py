import tkinter as tk
from tkinter import ttk
import threading
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress
import json
import argostranslate.package
import argostranslate.translate
import torch
import subprocess
import os
import ffmpeg
import subprocess
import time


def on_button_click(user_url, target_lang, label):
    # Update the label to inform the user to wait
    label.config(text="Wait for the translation please...")

    # Start the translation process in a separate thread
    threading.Thread(target=perform_translation, args=(user_url, target_lang, label)).start()

def perform_translation(user_url, target_lang, label):
    start_time = time.time()

    url = user_url

    desktop = os.getcwd()

    yt = YouTube(url, on_progress_callback=on_progress)
    # Download the video that has the highest quality
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

    video_stream.download(filename='video.mp4', output_path=desktop)
    audio_stream.download(filename='audio.mp4', output_path=desktop)

    subprocess.run(["ffmpeg", "-i", os.path.join(desktop, "audio.mp4"), os.path.join(desktop, "audio.mp3")])
    subprocess.run(["ffmpeg", "-i", os.path.join(desktop, "video.mp4"), "-i", os.path.join(desktop, "audio.mp4"), "-c", "copy", os.path.join(desktop, "your_video.mp4")])

    subprocess.run(["whisperx", os.path.join(desktop, "audio.mp3"), "--compute_type", "int8", "--output_format", "srt"])
    end_time = time.time()
    print(end_time - start_time)

    to_code = target_lang
    from_code = "en"

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
       filter(
         lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    
    f = open(os.path.join(desktop, "audio.srt"), "r")
    data = f.readlines()

    srt = open(os.path.join(desktop, "subtitle.srt"), "w")
    # Translate
    for i in range(len(data)):
        if i % 4 == 2:
            translatedText = argostranslate.translate.translate(data[i], from_code, to_code)
            srt.write(translatedText)
            print("accessed")
        else:
            srt.write(data[i])
    srt.close()

    
    # Update the label after the translation is done
    label.config(text="Your video and subtitle are ready!")

# Create the main application window
root = tk.Tk()
root.title("Subtitler")

# Create a text input field
text_input = ttk.Entry(root, width=30)
text_input.grid(row=0, column=1, padx=10, pady=10)

# Create a dropdown menu
dropdown_var = tk.StringVar()
dropdown_var.set("en")  # Set default value
dropdown_menu = ttk.OptionMenu(root, dropdown_var, "en", "fr", "de", "es")
dropdown_menu.grid(row=1, column=1, padx=10, pady=10)

# Create a status label to show translation status
status_label = ttk.Label(root, text="")
status_label.grid(row=3, column=1, padx=10, pady=10)

# Create a button
button = ttk.Button(root, text="Translate", command=lambda: on_button_click(text_input.get(), dropdown_var.get(), status_label))
button.grid(row=2, column=1, padx=10, pady=10)

# Create labels for better UI
label1 = ttk.Label(root, text="Enter URL:")
label1.grid(row=0, column=0, padx=10, pady=10)

label2 = ttk.Label(root, text="Choose Language:")
label2.grid(row=1, column=0, padx=10, pady=10)

# Run the application
root.mainloop()
