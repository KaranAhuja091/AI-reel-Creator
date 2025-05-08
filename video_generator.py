from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from PIL import ImageFont, ImageDraw, Image
import os

# Constants
WIDTH = 1080
HEIGHT = 1920
DURATION = 5  # seconds
FONT_SIZE = 80
FONT_COLOR = 'white'
BACKGROUND_COLOR = (0, 0, 0)
FPS = 24
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update for your system if needed

def generate_video(text: str, output_path="output.mp4"):
    # Create an image with text using PIL
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print("Could not load font. Using default.")
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(text, font=font)
    x = (WIDTH - text_width) / 2
    y = (HEIGHT - text_height) / 2
    draw.text((x, y), text, fill=FONT_COLOR, font=font)

    # Save image temporarily
    temp_image_path = "temp_text_image.png"
    image.save(temp_image_path)

    # Create a video clip from the image
    image_clip = (ImageClip(temp_image_path)
                  .set_duration(DURATION)
                  .set_fps(FPS))

    # Optional: Add background color layer
    background = ColorClip(size=(WIDTH, HEIGHT), color=BACKGROUND_COLOR, duration=DURATION)
    final_clip = CompositeVideoClip([background, image_clip])

    # Export the video
    final_clip.write_videofile(output_path, codec="libx264", fps=FPS)

    # Clean up
    os.remove(temp_image_path)

if __name__ == "__main__":
    generate_video("Hello, this is a test reel!")
