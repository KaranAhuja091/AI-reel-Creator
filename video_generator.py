from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
import os

def generate_image_with_text(text, output_path="frame.png"):
    # Create a blank white image
    width, height = 720, 1280
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Load default font
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Word wrap logic (basic)
    max_width = width - 100
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    # Center the text
    y_text = height // 2 - len(lines) * 30
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) // 2
        draw.text((x, y_text), line, font=font, fill='black')
        y_text += 70

    image.save(output_path)
    print(f"Image saved to {output_path}")

def generate_video_from_image(image_path, video_path="output_video.mp4", duration=5):
    clip = ImageClip(image_path).set_duration(duration)
    clip = clip.set_fps(24)
    clip.write_videofile(video_path, codec="libx264", audio=False)
    print(f"Video saved to {video_path}")

if __name__ == "__main__":
    text_input = "This is a sample short generated from text using Pillow and MoviePy!"
    image_file = "frame.png"
    video_file = "output_video.mp4"

    generate_image_with_text(text_input, image_file)
    generate_video_from_image(image_file, video_file)
