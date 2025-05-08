from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

def generate_image_with_text(text, output_path="frame.png"):
    width, height = 720, 1280
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

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
    if line:
        lines.append(line)

    total_text_height = len(lines) * 70
    y_text = (height - total_text_height) // 2

    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) // 2
        draw.text((x, y_text), line, font=font, fill='black')
        y_text += 70

    image.save(output_path)
    return output_path

def generate_video_from_image(image_path, video_path="output_video.mp4", duration=5):
    clip = ImageClip(image_path).set_duration(duration)
    clip = clip.set_fps(24)
    clip.write_videofile(video_path, codec="libx264", audio=False)
    return video_path

def generate_video(text, image_path="frame.png", video_path="output_video.mp4", duration=5):
    img_path = generate_image_with_text(text, image_path)
    vid_path = generate_video_from_image(img_path, video_path, duration)
    return vid_path

# Optional: for testing directly
if __name__ == "__main__":
    sample_text = "This is a test short made from plain text using Pillow and MoviePy."
    generate_video(sample_text)
