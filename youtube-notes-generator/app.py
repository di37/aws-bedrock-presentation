import os
import streamlit as st

from client import client
from utils import MODEL_LLAMA_3_1_8B, MODEL_LLAMA_3_1_70B, MODEL_LLAMA_3_1_405B
from utils import youtube_transcriber, invoke_model_llama_stream
from utils import SYSTEM_PROMPT_NOTE_GEN, user_prompt_note_gen
from custom_logger import logger

st.set_page_config(page_title="▶️ YouTube Audio Notes Generator", page_icon="🎵📝")

st.title("▶️ YouTube Notes Generator 📝")
st.markdown("Transform your YouTube videos into detailed notes with AI! 🚀")

# Initialize session state
if "generated_notes" not in st.session_state:
    st.session_state.generated_notes = ""
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# Sidebar inputs
with st.sidebar:
    st.header("📊 Input Parameters")
    youtube_url = st.text_input(
        "🔗 YouTube URL", placeholder="Paste your YouTube URL here..."
    )
    # Temperature slider
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness. Lower values make the model more deterministic, higher values make it more random.",
    )

    # Top-p (nucleus sampling) slider
    top_p = st.sidebar.slider(
        "Top-p",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1,
        help="Controls diversity via nucleus sampling. 1.0 means no nucleus sampling.",
    )

    # Max generation length slider
    max_length = st.sidebar.slider(
        "Max Generation Length",
        min_value=1,
        max_value=8192,
        value=512,
        step=1,
        help="Maximum number of tokens to generate.",
    )
    model_name = st.selectbox(
        "🤖 Model Name", [MODEL_LLAMA_3_1_8B, MODEL_LLAMA_3_1_70B, MODEL_LLAMA_3_1_405B]
    )
    generate_button = st.button("🚀 Generate Notes", use_container_width=True)

    # Add a clear button
    clear_button = st.button("🧹 Clear Notes", use_container_width=True)

    if st.session_state.show_download:
        st.download_button(
            label="📥 Download Notes as MD",
            data=st.session_state.generated_notes,
            file_name="notes.md",
            mime="text/markdown",
            use_container_width=True,
        )

# Main content area
st.header("📄 Generated Notes")

# Handle clear button click
if clear_button:
    st.session_state.generated_notes = ""
    st.session_state.show_download = False
    st.rerun()

if generate_button:
    text_transcript = youtube_transcriber(youtube_url)
    user_prompt = user_prompt_note_gen(text_transcript)
    if youtube_url and model_name and SYSTEM_PROMPT_NOTE_GEN and user_prompt:
        with st.spinner("🔄 Generating notes... Please wait."):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in invoke_model_llama_stream(
                client=client,
                system_prompt=SYSTEM_PROMPT_NOTE_GEN,
                user_prompt=user_prompt,
                model_id=model_name,
                max_gen_len=max_length,
                temperature=temperature,
                top_p=top_p,
            ):
                full_response += chunk
                response_placeholder.markdown(full_response)

        logger.info("Response successfully generated.")

        # Store generated notes in session state and show download button
        st.session_state.generated_notes = full_response
        st.session_state.show_download = True
        st.rerun()  # Rerun the app to update the sidebar

# Always display the generated notes if they exist
if st.session_state.generated_notes:
    st.markdown(st.session_state.generated_notes)
else:
    st.info("👆 Click 'Generate Notes' in the sidebar to start the process!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Isham Rashik | [GitHub](https://github.com/di37)")
