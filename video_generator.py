from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips
import tempfile
import os

def generate_video(texts, output_path='output_video.mp4', duration_per_slide=3):
    W, H = 1080, 1920
    bg_color = (0, 0, 0)
    text_color = (255, 255, 255)

    # Try to load a system font, fallback to default
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    except OSError:
        font = ImageFont.load_default()

    image_clips = []

    for idx, text in enumerate(texts):
        img = Image.new("RGB", (W, H), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Handle modern PIL with textbbox
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # For older PIL versions
            text_width, text_height = draw.textsize(text, font=font)

        position = ((W - text_width) // 2, (H - text_height) // 2)
        draw.text(position, text, fill=text_color, font=font)

        temp_img_path = os.path.join(tempfile.gettempdir(), f"frame_{idx}.png")
        img.save(temp_img_path)

        clip = ImageClip(temp_img_path).set_duration(duration_per_slide)
        image_clips.append(clip)

    final_clip = concatenate_videoclips(image_clips, method="compose")
    final_clip.write_videofile(output_path, fps=24)

    return output_path
