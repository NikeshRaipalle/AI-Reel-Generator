import os
import subprocess
import sys
import requests
import zipfile

def download_ffmpeg():
    """Download and setup FFmpeg"""
    print("Setting up FFmpeg...")
    
    # Check if ffmpeg.exe already exists
    if os.path.exists("ffmpeg.exe"):
        print("FFmpeg already exists!")
        return True
    
    try:
        # Download portable FFmpeg
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        print("Downloading FFmpeg...")
        
        response = requests.get(url, stream=True)
        with open("ffmpeg.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract FFmpeg
        print("Extracting FFmpeg...")
        with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
        
        # Find and copy ffmpeg.exe
        for root, dirs, files in os.walk("temp_ffmpeg"):
            if "ffmpeg.exe" in files:
                ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                os.rename(ffmpeg_path, "ffmpeg.exe")
                break
        
        # Cleanup
        os.remove("ffmpeg.zip")
        import shutil
        shutil.rmtree("temp_ffmpeg")
        
        print("FFmpeg setup complete!")
        return True
        
    except Exception as e:
        print(f"Error setting up FFmpeg: {e}")
        print("Please download FFmpeg manually from https://ffmpeg.org/download.html")
        return False

if __name__ == "__main__":
    download_ffmpeg()