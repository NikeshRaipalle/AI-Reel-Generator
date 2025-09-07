from flask import Flask, render_template,request
import uuid
from werkzeug.utils import secure_filename
import os
import subprocess
from text_to_audio import text_to_speech_file
import mutagen.mp3

UPLOAD_FOLDER='user_uploads'
ALLOWED_EXTENSIONS={'png','jpg','jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route("/")
def home():
    # Get recent reels for showcase
    try:
        reels = os.listdir("static/reels")
        recent_reels = reels[:5]  # Show only first 5 reels
    except:
        recent_reels = []
    return render_template("index.html", recent_reels=recent_reels)

@app.route("/create",methods=["GET","POST"])
def create():
    myid=uuid.uuid1()
    if request.method=="POST":
        print(request.files.keys())
        rec_id=request.form.get("uuid")
        desc=request.form.get("text")
        input_files=[]
        for key,value in request.files.items():
            print(key,value)
            #upload the file
            file=request.files[key]
            if file:
                filename=secure_filename(file.filename)
                if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],rec_id)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,filename))
                input_files.append(file.filename)
            #Capture the description and save it to a file
            with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,"desc.txt"),"w") as f:
                f.write(desc)
        # Calculate duration per image based on text length
        text_length = len(desc.split())
        duration_per_image = max(2, text_length / len(input_files) * 0.5)  # At least 2 seconds per image
        
        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id,"input.txt"), "a") as f:
                f.write(f"file '{fl}'\n duration {duration_per_image}\n")
        
        # Create reel immediately after upload
        if input_files and desc:
            try:
                create_reel_now(rec_id)
            except Exception as e:
                print(f"Error creating reel: {e}")

    return render_template("create.html",myid=myid)

def create_reel_now(folder_id):
    """Create reel immediately after upload"""
    try:
        # Generate audio
        with open(f"user_uploads/{folder_id}/desc.txt") as f:
            text = f.read()
        text_to_speech_file(text, folder_id)
        
        # Get audio duration and update input.txt with proper timing
        try:
            from mutagen.mp3 import MP3
            audio = MP3(f"user_uploads/{folder_id}/audio.mp3")
            audio_duration = audio.info.length
        except:
            # Fallback: estimate duration based on text (average 150 words per minute)
            words = len(text.split())
            audio_duration = max(5, words / 150 * 60)  # At least 5 seconds
        
        # Count images and recalculate duration
        with open(f"user_uploads/{folder_id}/input.txt", "r") as f:
            lines = f.readlines()
        
        image_count = len([line for line in lines if line.startswith("file")])
        duration_per_image = audio_duration / image_count if image_count > 0 else 2
        
        # Rewrite input.txt with correct durations
        with open(f"user_uploads/{folder_id}/input.txt", "w") as f:
            for line in lines:
                if line.startswith("file"):
                    f.write(line)
                    f.write(f"duration {duration_per_image}\n")
        
        # Create video
        ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
        command = f'''{ffmpeg_cmd} -f concat -safe 0 -i user_uploads/{folder_id}/input.txt -i user_uploads/{folder_id}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder_id}.mp4'''
        
        subprocess.run(command, shell=True, check=True)
        
        # Mark as done
        with open("done.txt", "a") as f:
            f.write(folder_id + "\n")
            
        print(f"Reel created successfully: {folder_id} (Duration: {audio_duration:.1f}s)")
        
    except Exception as e:
        print(f"Error creating reel for {folder_id}: {e}")
        raise e

@app.route("/music-integration", methods=["GET", "POST"])
def music_integration():
    if request.method == "POST":
        reel_id = request.form.get("reel_id")
        music_type = request.form.get("music_type")
        volume = request.form.get("volume", "0.5")
        
        try:
            output_name = add_music_to_reel(reel_id, music_type, float(volume))
            return {"status": "success", "message": f"Music added: {output_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    reels = os.listdir("static/reels")
    return render_template("music_integration.html", reels=reels)

def add_music_to_reel(reel_id, music_type, volume):
    """Add background music to reel"""
    import time
    output_name = f"music_{int(time.time())}.mp4"
    output_path = f"static/reels/{output_name}"
    input_path = f"static/reels/{reel_id}"
    ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
    
    if music_type == "upbeat":
        # Generate upbeat background tone
        command = f'{ffmpeg_cmd} -i {input_path} -f lavfi -i "sine=frequency=440:duration=30" -filter_complex "[1:a]volume={volume}[bg];[0:a][bg]amix=inputs=2" -c:v copy -shortest {output_path}'
    elif music_type == "chill":
        # Generate chill background tone
        command = f'{ffmpeg_cmd} -i {input_path} -f lavfi -i "sine=frequency=220:duration=30" -filter_complex "[1:a]volume={volume}[bg];[0:a][bg]amix=inputs=2" -c:v copy -shortest {output_path}'
    else:
        # Add ambient sound
        command = f'{ffmpeg_cmd} -i {input_path} -f lavfi -i "anoisesrc=duration=30:color=brown" -filter_complex "[1:a]volume={volume}[bg];[0:a][bg]amix=inputs=2" -c:v copy -shortest {output_path}'
    
    subprocess.run(command, shell=True, check=True)
    return output_name

@app.route("/smart-stitch", methods=["GET", "POST"])
def smart_stitch():
    if request.method == "POST":
        selected_reels = request.form.getlist("reels")
        stitch_type = request.form.get("stitch_type")
        
        try:
            output_name = stitch_reels(selected_reels, stitch_type)
            return {"status": "success", "message": f"Stitched reel created: {output_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    reels = os.listdir("static/reels")
    return render_template("smart_stitch.html", reels=reels)

def stitch_reels(selected_reels, stitch_type):
    """Smart stitching of multiple reels"""
    import time
    output_name = f"stitched_{int(time.time())}.mp4"
    output_path = f"static/reels/{output_name}"
    ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
    
    # Create input list file
    with open("temp_stitch_list.txt", "w") as f:
        for reel in selected_reels:
            f.write(f"file 'static/reels/{reel}'\n")
    
    if stitch_type == "fade":
        # Fade transitions between clips
        command = f'{ffmpeg_cmd} -f concat -safe 0 -i temp_stitch_list.txt -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=5:d=0.5" -c:a aac {output_path}'
    elif stitch_type == "crossfade":
        # Crossfade audio and video
        command = f'{ffmpeg_cmd} -f concat -safe 0 -i temp_stitch_list.txt -af "acrossfade=d=1" {output_path}'
    else:
        # Simple concatenation
        command = f'{ffmpeg_cmd} -f concat -safe 0 -i temp_stitch_list.txt -c copy {output_path}'
    
    subprocess.run(command, shell=True, check=True)
    os.remove("temp_stitch_list.txt")
    return output_name

@app.route("/ai-edit", methods=["GET", "POST"])
def ai_edit():
    if request.method == "POST":
        # Get the reel ID to enhance
        reel_id = request.form.get("reel_id")
        enhancement_type = request.form.get("enhancement")
        
        try:
            enhance_reel(reel_id, enhancement_type)
            return {"status": "success", "message": f"Reel enhanced with {enhancement_type}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Get available reels for enhancement
    reels = os.listdir("static/reels")
    return render_template("ai_edit.html", reels=reels)

def enhance_reel(reel_id, enhancement_type):
    """AI-powered reel enhancement"""
    input_video = f"static/reels/{reel_id}"
    output_video = f"static/reels/enhanced_{reel_id}"
    ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
    
    if enhancement_type == "brightness":
        # Auto brightness adjustment
        command = f'{ffmpeg_cmd} -i {input_video} -vf "eq=brightness=0.1:contrast=1.2" -c:a copy {output_video}'
    elif enhancement_type == "stabilize":
        # Video stabilization
        command = f'{ffmpeg_cmd} -i {input_video} -vf "vidstabdetect=shakiness=10:accuracy=10" -f null - && {ffmpeg_cmd} -i {input_video} -vf "vidstabtransform=smoothing=10" -c:a copy {output_video}'
    elif enhancement_type == "speed":
        # Smart speed adjustment
        command = f'{ffmpeg_cmd} -i {input_video} -filter:v "setpts=0.8*PTS" -filter:a "atempo=1.25" {output_video}'
    else:
        # Default: color enhancement
        command = f'{ffmpeg_cmd} -i {input_video} -vf "eq=contrast=1.1:brightness=0.05:saturation=1.2" -c:a copy {output_video}'
    
    subprocess.run(command, shell=True, check=True)
    print(f"Enhanced reel created: enhanced_{reel_id}")

@app.route("/gallery")
def gallery():
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html",reels=reels)

app.run(debug=True)