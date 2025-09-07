#this file looks for new file in user uploads and converts them into reel if they are not already converted
import os
from text_to_audio import text_to_speech_file
import time
import subprocess
from mutagen.mp3 import MP3


def text_to_audio(folder):
  print("TTA -",folder)
  with open(f"user_uploads/{folder}/desc.txt") as f:
    text=f.read()
  print(text,folder)
  text_to_speech_file(text,folder)

def create_reel(folder):
  # Get audio duration and fix input.txt timing
  try:
    audio = MP3(f"user_uploads/{folder}/audio.mp3")
    audio_duration = audio.info.length
  except:
    # Fallback: read text and estimate
    with open(f"user_uploads/{folder}/desc.txt") as f:
      text = f.read()
    words = len(text.split())
    audio_duration = max(5, words / 150 * 60)
  
  # Fix input.txt with proper duration
  with open(f"user_uploads/{folder}/input.txt", "r") as f:
    lines = f.readlines()
  
  image_count = len([line for line in lines if line.startswith("file")])
  duration_per_image = audio_duration / image_count if image_count > 0 else 2
  
  # Rewrite input.txt
  with open(f"user_uploads/{folder}/input.txt", "w") as f:
    for line in lines:
      if line.startswith("file"):
        f.write(line)
        f.write(f"duration {duration_per_image}\n")
  
  # Use local ffmpeg.exe if available, otherwise try system ffmpeg
  ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
  
  command=f'''{ffmpeg_cmd} -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
  
  try:
    subprocess.run(command,shell=True,check=True)
    print(f"CR - Reel created successfully: {folder} (Duration: {audio_duration:.1f}s)")
  except subprocess.CalledProcessError as e:
    print(f"Error creating reel for {folder}: {e}")
    print("Make sure FFmpeg is installed. Run: python fix_reel_creation.py")
    raise e

if __name__=="__main__":
    while True:
      print("Processing queue...")
      with open("done.txt","r") as f:
        done_folders=f.readlines()

      done_folders=[f.strip() for f in done_folders]
      folders=os.listdir("user_uploads")
      for folder in folders:
        if(folder not in done_folders):
          text_to_audio(folder) #Generate the audio from desc.txt
          create_reel(folder) #Convert the images and audio.mp inside the folder to a reel
          with open("done.txt","a") as f:
            f.write(folder + "\n")
      time.sleep(4)