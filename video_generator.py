from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips
import os
import tempfile

def generate_video(texts, output_path='output_video.mp4', duration_per_slide=3):
    """
    Generate a vertical short-form video from a list of text strings.

    :param texts: List of text strings (e.g., ["Tip 1: Use strong hooks", "Tip 2: Keep it short"])
    :param output_path: Path to save the final video
    :param duration_per_slide: Duration of each text slide in seconds
    """

    W, H = 1080, 1920  # Vertical resolution for Reels/Shorts
    bg_color = (0, 0, 0)
    text_color = (255, 255, 255)

    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except OSError:
        font = ImageFont.load_default()

    image_clips = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, text in enumerate(texts):
            img = Image.new("RGB", (W, H), color=bg_color)
            draw = ImageDraw.Draw(img)

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((W - text_width) // 2, (H - text_height) // 2)

            draw.text(position, text, fill=text_color, font=font)

            img_path = os.path.join(tmpdir, f"frame_{idx}.png")
            img.save(img_path)

            clip = ImageClip(img_path).set_duration(duration_per_slide)
            image_clips.append(clip)

        final_clip = concatenate_videoclips(image_clips, method="compose")
        final_clip.write_videofile(output_path, fps=24, audio=False)

# Example usage
if __name__ == '__main__':
    sample_texts = ["Tip 1: Use strong hooks", "Tip 2: Keep it short", "Tip 3: Add subtitles"]
    generate_video(sample_texts, output_path="sample_video.mp4")
