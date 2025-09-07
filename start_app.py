import subprocess
import threading
import time
import os

def run_flask_app():
    """Run the Flask application"""
    print("Starting Flask app...")
    subprocess.run(["python", "main.py"])

def run_processor():
    """Run the reel generation processor"""
    print("Starting reel processor...")
    time.sleep(3)  # Wait for Flask to start
    subprocess.run(["python", "generate_process.py"])

def main():
    print("=== AI Reels Maker ===")
    print("Setting up the application...")
    
    # Check if FFmpeg exists
    if not os.path.exists("ffmpeg.exe"):
        print("FFmpeg not found. Please run: python fix_reel_creation.py")
        print("Or download FFmpeg manually and place ffmpeg.exe in this directory")
        return
    
    print("FFmpeg found!")
    print("Starting both Flask app and reel processor...")
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start processor in a separate thread
    processor_thread = threading.Thread(target=run_processor)
    processor_thread.daemon = True
    processor_thread.start()
    
    print("Application started!")
    print("Flask app: http://127.0.0.1:5000")
    print("Reel processor is running in background")
    print("Press Ctrl+C to stop")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()