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

desktop = os.getcwd()
def download(user_url):
    url = user_url

    yt = YouTube(url, on_progress_callback=on_progress)
    # Download the video that has the highest quality
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

    video_stream.download(filename='video.mp4', output_path=desktop)
    audio_stream.download(filename='audio.mp4', output_path=desktop)

def merge_audio_and_video():    
    subprocess.run(["ffmpeg", "-i", os.path.join(desktop, "audio.mp4"), os.path.join(desktop, "audio.mp3")])
    subprocess.run(["ffmpeg", "-i", os.path.join(desktop, "video.mp4"), "-i", os.path.join(desktop, "audio.mp4"), "-c", "copy", os.path.join(desktop, "your_video.mp4")])

    try:
        
        os.remove(os.path.join(desktop,"audio.mp4"))
        os.remove(os.path.join(desktop,"video.mp4"))
    except:
        print("files cannot be found")

def transcribe_video():
    subprocess.run(["whisperx", os.path.join(desktop, "audio.mp3"), "--compute_type", "int8", "--output_format", "srt"])

    try:
        os.remove(os.path.join(desktop,"audio.mp3"))
    except:
        print("audio file cannot be found for whisperx")

def translate(target_lang):
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
    for i in range(len(data)):#TODO make this line faster 
        if i % 4 == 2:
            translatedText = argostranslate.translate.translate(data[i], from_code, to_code)
            srt.write(translatedText)
            print("accessed")
        else:
            srt.write(data[i])
    srt.close()
    f.close()
    try:
        os.remove(os.path.join(desktop,"audio.srt"))
    except:
        print("audio.srt cannot be found")


def perform_translation(url_dict, label):
    i = 1
    for pair in url_dict:
        download(pair)
        merge_audio_and_video()
        transcribe_video()
        translate(url_dict[pair])
        os.rename(os.path.join(desktop,"your_video.mp4"), f"{i}.mp4")
        os.rename(os.path.join(desktop,"subtitle.srt"), f"{i}.srt")
        i+=1

    label.config(text="Your video and subtitle are ready!")