import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, CompositeVideoClip
from PIL import Image
import os

def process_video(video_path, png_path):
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Remove the sound from the video
    video_no_sound = video.without_audio()
    
    # Reverse the video
    video_reversed = video_no_sound.fx(lambda clip: clip.fx(vfx.time_mirror))
    
    # Create a composite video with the PNG overlay
    overlay = Image.open(png_path)
    overlay_clip = ImageClip(overlay).set_duration(video_no_sound.duration).set_position("center").resize(video_no_sound.size)
    
    # Concatenate the original and reversed videos
    final_video = concatenate_videoclips([video_no_sound, video_reversed])
    
    # Overlay the PNG
    final_video_with_overlay = CompositeVideoClip([final_video, overlay_clip])
    
    # Save the final video
    folder, filename = os.path.split(video_path)
    basename, ext = os.path.splitext(filename)
    output_path = os.path.join(folder, f"NFT-{basename}{ext}")
    final_video_with_overlay.write_videofile(output_path, codec='libx264')

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        png_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if png_path:
            process_video(file_path, png_path)

# Create the Tkinter GUI
root = tk.Tk()
root.withdraw()  # Hide the main window
select_file()  # Trigger the file selection dialog
