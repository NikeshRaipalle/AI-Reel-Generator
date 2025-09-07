import os
from text_to_audio import text_to_speech_file
import subprocess

def process_pending_reels():
    """Process all pending reel uploads"""
    print("Processing pending reels...")
    
    # Check if FFmpeg exists
    ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
    
    # Read done folders
    try:
        with open("done.txt", "r") as f:
            done_folders = [f.strip() for f in f.readlines()]
    except FileNotFoundError:
        done_folders = []
    
    # Get all upload folders
    folders = os.listdir("user_uploads")
    pending_folders = [f for f in folders if f not in done_folders]
    
    if not pending_folders:
        print("No pending reels to process!")
        return
    
    print(f"Found {len(pending_folders)} pending reels:")
    for folder in pending_folders:
        print(f"  - {folder}")
    
    # Process each pending folder
    for folder in pending_folders:
        try:
            print(f"\nProcessing {folder}...")
            
            # Generate audio from text
            print("  Generating audio...")
            with open(f"user_uploads/{folder}/desc.txt") as f:
                text = f.read()
            text_to_speech_file(text, folder)
            
            # Create reel
            print("  Creating video...")
            command = f'''{ffmpeg_cmd} -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
            
            subprocess.run(command, shell=True, check=True)
            
            # Mark as done
            with open("done.txt", "a") as f:
                f.write(folder + "\n")
            
            print(f"  ✓ Reel created: {folder}.mp4")
            
        except Exception as e:
            print(f"  ✗ Error processing {folder}: {e}")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    process_pending_reels()