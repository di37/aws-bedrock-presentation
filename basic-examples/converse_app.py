import streamlit as st
from client import client as bedrock_client
from utils import (
    MODEL_LLAMA_3_1_8B,
    MODEL_LLAMA_3_1_70B,
    MODEL_LLAMA_3_1_405B,
)
from utils import SYSTEM_PROMPT_LLAMA
from utils import converse_llama_stream

from custom_logger import logger


def clear_chat_history():
    st.session_state.messages = []
    logger.info("Cleared chat history.")


def main():
    st.title("AWS Bedrock Chat Application")

    st.sidebar.header("Adjust Parameters")

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

    model_selection = st.sidebar.selectbox(
        "Model Selection",
        [
            MODEL_LLAMA_3_1_8B,
            MODEL_LLAMA_3_1_70B,
            MODEL_LLAMA_3_1_405B,
        ],
    )

    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        clear_chat_history()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Prepare messages for the model
        model_messages = [
            {"role": msg["role"], "content": [{"text": msg["content"]}]}
            for msg in st.session_state.messages
        ]

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for response_chunk in converse_llama_stream(
                bedrock_client=bedrock_client,
                model_id=model_selection,
                system_prompts=[{"text": SYSTEM_PROMPT_LLAMA}],
                messages=model_messages,
                max_gen_len=max_length,
                temperature=temperature,
                top_p=top_p,
            ):
                full_response += response_chunk
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":
    main()
