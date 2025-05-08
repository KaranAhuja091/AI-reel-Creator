# ai-reel-generator/video_generator.py
from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile
import os

def generate_video(text, audio_path, duration=10, resolution=(720, 1280)):
    # Create a blank image with black background
    img = Image.new('RGB', resolution, color='black')
    draw = ImageDraw.Draw(img)

    # Load a font (change to path if needed)
    try:
        font = ImageFont.truetype("Arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Wrap text to fit within the image width
    margin = 40
    wrapped_text = textwrap.fill(text, width=40)

    # Calculate text size using textbbox (instead of textsize)
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate position for centered text
    text_x = (resolution[0] - text_width) / 2
    text_y = (resolution[1] - text_height) / 2
    draw.text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255))

    # Save image temporarily
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_img.name)

    # Create video clip from image
    clip = ImageClip(temp_img.name).set_duration(duration)

    # Add audio
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio).set_duration(audio.duration)

    # Save video
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    clip.write_videofile(output_path, fps=24)

    return output_path
