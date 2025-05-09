import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips

def generate_video(texts, output_path='output_video.mp4', duration_per_slide=3):
    """
    Generate a vertical short-form video from a list of text strings.
    """
    if not texts:
        raise ValueError("Input text list is empty. Cannot generate video.")

    W, H = 1080, 1920  # Vertical resolution for Reels/Shorts
    bg_color = (0, 0, 0)
    text_color = (255, 255, 255)

    # Font fallback handling
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except OSError:
        font = ImageFont.load_default()

    image_clips = []

    os.makedirs("/tmp/frames", exist_ok=True)

    for idx, text in enumerate(texts):
        img = Image.new("RGB", (W, H), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Text centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((W - text_width) // 2, (H - text_height) // 2)
        draw.text(position, text, fill=text_color, font=font)

        img_path = f"/tmp/frames/frame_{idx}.png"
        img.save(img_path)

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not created: {img_path}")

        clip = ImageClip(img_path).set_duration(duration_per_slide)
        image_clips.append(clip)

    if not image_clips:
        raise RuntimeError("No image clips generated. Aborting video creation.")

    final_clip = concatenate_videoclips(image_clips, method="compose")

    try:
        final_clip.write_videofile(output_path, fps=24)
    except Exception as e:
        raise RuntimeError(f"FFmpeg error during video writing: {e}")
