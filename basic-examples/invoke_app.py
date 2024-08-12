import streamlit as st
from utils import invoke_model_llama, invoke_model_llama_stream
from utils import MODEL_LLAMA_3_1_8B, MODEL_LLAMA_3_1_70B, MODEL_LLAMA_3_1_405B


def main():
    st.title("🌩️ Amazon Bedrock Text Gen Application")

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
        [MODEL_LLAMA_3_1_8B, MODEL_LLAMA_3_1_70B, MODEL_LLAMA_3_1_405B],
    )

    # Streaming option
    is_streaming = st.sidebar.checkbox("Enable streaming output", value=False)

    # Input prompt in sidebar
    user_input = st.sidebar.text_area(
        "Enter Your Prompt", "Enter your text here...", height=150
    )

    # Generate button in sidebar
    generate_button = st.sidebar.button("Generate")

    # Create a placeholder for the output
    output_placeholder = st.empty()

    if generate_button:
        if is_streaming:
            # Streaming output
            output_placeholder.markdown("Generating text...")
            full_response = ""
            for chunk in invoke_model_llama_stream(
                prompt=user_input,
                model_id=model_selection,
                max_gen_len=max_length,
                temperature=temperature,
                top_p=top_p,
            ):
                full_response += chunk
                output_placeholder.markdown(full_response + "▌")
        else:
            # Non-streaming output
            with st.spinner("Generating text... Please wait."):
                response = invoke_model_llama(
                    prompt=user_input,
                    model_id=model_selection,
                    max_gen_len=max_length,
                    temperature=temperature,
                    top_p=top_p,
                )
            output_placeholder.markdown(response)


if __name__ == "__main__":
    main()
