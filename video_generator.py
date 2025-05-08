from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import tempfile

def generate_video(text, audio_path, duration=10, resolution=(720, 1280)):
    clip = TextClip(text, fontsize=40, color='white', bg_color='black', size=resolution, method='caption')
    clip = clip.set_duration(duration).set_position('center')

    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio).set_duration(audio.duration)

    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    clip.write_videofile(output_path, fps=24)
    return output_path
