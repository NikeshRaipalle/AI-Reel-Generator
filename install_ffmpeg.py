import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil

def install_ffmpeg():
    """Install FFmpeg on Windows"""
    print("Installing FFmpeg...")
    
    # Create ffmpeg directory
    ffmpeg_dir = "ffmpeg"
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(ffmpeg_dir)
    
    # Download FFmpeg
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"
    
    print("Downloading FFmpeg...")
    try:
        urllib.request.urlretrieve(ffmpeg_url, zip_path)
        
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # Find the extracted folder
        extracted_folders = [f for f in os.listdir(ffmpeg_dir) if f.startswith('ffmpeg-')]
        if extracted_folders:
            extracted_path = os.path.join(ffmpeg_dir, extracted_folders[0], 'bin')
            
            # Copy ffmpeg.exe to current directory
            ffmpeg_exe = os.path.join(extracted_path, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_exe):
                shutil.copy2(ffmpeg_exe, 'ffmpeg.exe')
                print("FFmpeg installed successfully!")
                
                # Clean up
                os.remove(zip_path)
                shutil.rmtree(ffmpeg_dir)
                return True
        
        print("Error: Could not find FFmpeg executable")
        return False
        
    except Exception as e:
        print(f"Error installing FFmpeg: {e}")
        return False

if __name__ == "__main__":
    install_ffmpeg()