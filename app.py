import streamlit as st
from summarizer import summarize_text
from tts import text_to_speech
from video_generator import generate_video
import os

st.set_page_config(page_title="AI Reels Generator", layout="centered")
st.title("🎬 AI Reel/Shorts Generator")

input_text = st.text_area("Paste long text, blog, or script:", height=250)

if st.button("Generate Reel"):
    if input_text.strip() == "":
        st.warning("Please paste some text to summarize and generate the video.")
    else:
        with st.spinner("Summarizing content..."):
            summary = summarize_text(input_text)
            st.success("Summary generated")

        with st.spinner("Generating voiceover..."):
            audio_path = text_to_speech(summary)
            st.success("Voiceover created")

        with st.spinner("Creating vertical video..."):
            output_path = generate_video(summary, audio_path)
            st.success("Reel created successfully!")

        st.video(output_path)
        st.download_button("📥 Download Video", data=open(output_path, "rb").read(), file_name="reel.mp4")
