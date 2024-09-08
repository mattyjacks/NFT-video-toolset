import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx  # Import the vfx module
import os
from PIL import Image  # Ensure PIL is imported correctly

# Initialize main Tkinter window
root = tk.Tk()
root.title("NFT Video Toolset")

# Global variables for video path and overlay path
video_path = None
overlay_path = None

# File selectors
def select_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov")])
    video_label.config(text=os.path.basename(video_path))

def select_overlay():
    global overlay_path
    overlay_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    overlay_label.config(text=os.path.basename(overlay_path))

# Process video: play twice, reverse second, add overlay
def process_video():
    if video_path:
        # Load the video
        video = VideoFileClip(video_path)

        # Create the reversed clip
        reverse_clip = video.fx(vfx.time_mirror)

        # Concatenate the normal and reversed clip
        final_clip = concatenate_videoclips([video, reverse_clip])

        # If an overlay is selected, add it to the video
        if overlay_path:
            overlay_img = ImageClip(overlay_path).set_duration(final_clip.duration)
            # Resize overlay to match video size using the latest Resampling method
            overlay_img = overlay_img.resize(final_clip.size)  
            final_clip = CompositeVideoClip([final_clip, overlay_img])

        # Save the final clip with "NFT-" prepended to the original filename
        original_filename = os.path.basename(video_path)
        output_filename = f"NFT-{original_filename}"
        save_path = os.path.join(os.path.dirname(video_path), output_filename)
        final_clip.write_videofile(save_path, codec="libx264", audio_codec="aac")
        result_label.config(text=f"Video saved as {output_filename}")

# UI elements
video_button = tk.Button(root, text="Select Video", command=select_video)
video_button.pack(pady=10)

video_label = tk.Label(root, text="No video selected")
video_label.pack()

overlay_button = tk.Button(root, text="Select PNG Overlay", command=select_overlay)
overlay_button.pack(pady=10)

overlay_label = tk.Label(root, text="No overlay selected")
overlay_label.pack()

run_button = tk.Button(root, text="Run", command=process_video)
run_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Start the Tkinter loop
root.mainloop()
