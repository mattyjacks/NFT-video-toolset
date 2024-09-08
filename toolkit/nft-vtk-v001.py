import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, font
from moviepy.editor import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# Initialize main Tkinter window
root = tk.Tk()
root.title("NFT Video Toolset")

# Global variables for video path and settings
video_path = None
overlay_path = None
watermark_text = ""
border_color = None

# File selectors
def select_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov")])
    video_label.config(text=os.path.basename(video_path))

def select_overlay():
    global overlay_path
    overlay_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    overlay_label.config(text=os.path.basename(overlay_path))

# Select watermark color
def select_color():
    global watermark_color
    watermark_color = colorchooser.askcolor()[1]
    color_label.config(text=f"Watermark Color: {watermark_color}")

# Video loop and reverse
def create_loop_clip(video):
    reverse_clip = video.fx(vfx.time_mirror)  # Reverse video
    final_clip = concatenate_videoclips([video, reverse_clip])  # Concatenate normal and reverse
    return final_clip

# Add watermark
def add_watermark(video, text, font_size, position, color, stroke_width, stroke_color):
    txt_clip = TextClip(text, fontsize=font_size, color=color, stroke_color=stroke_color, stroke_width=stroke_width, font="Arial")
    txt_clip = txt_clip.set_position(position).set_duration(video.duration)
    video = CompositeVideoClip([video, txt_clip])
    return video

# Add border
def add_border(clip, color, thickness):
    bordered_clip = clip.fx(vfx.margin, left=thickness, right=thickness, top=thickness, bottom=thickness, color=color)
    return bordered_clip

# Run the final video processing
def process_video():
    if video_path:
        video = VideoFileClip(video_path)
        final_clip = create_loop_clip(video)

        if overlay_path:
            overlay_img = Image.open(overlay_path)
            overlay_img = overlay_img.resize((video.size[0], video.size[1]))
            overlay_clip = ImageClip(overlay_img).set_duration(final_clip.duration)
            final_clip = CompositeVideoClip([final_clip, overlay_clip])

        if watermark_text:
            final_clip = add_watermark(final_clip, watermark_text, 50, 'center', watermark_color, 2, 'black')

        if border_color:
            final_clip = add_border(final_clip, border_color, 10)

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        final_clip.write_videofile(save_path, codec="libx264")

        progress_bar['value'] = 100

# UI elements
video_button = tk.Button(root, text="Select Video", command=select_video)
video_button.pack(pady=10)

video_label = tk.Label(root, text="No video selected")
video_label.pack()

overlay_button = tk.Button(root, text="Select PNG Overlay", command=select_overlay)
overlay_button.pack(pady=10)

overlay_label = tk.Label(root, text="No overlay selected")
overlay_label.pack()

color_button = tk.Button(root, text="Select Watermark Color", command=select_color)
color_button.pack(pady=10)

color_label = tk.Label(root, text="No color selected")
color_label.pack()

# Text input for watermark
watermark_entry = tk.Entry(root)
watermark_entry.pack(pady=10)
watermark_entry.insert(0, "Enter watermark text")

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

# Run button
run_button = tk.Button(root, text="Run", command=process_video)
run_button.pack(pady=10)

root.mainloop()
