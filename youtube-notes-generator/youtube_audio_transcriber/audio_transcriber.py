import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from dotenv import load_dotenv

from groq import Groq
import time

from custom_logger import logger

_ = load_dotenv()

start_time = time.time()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def transcribe_audio(input_filename):
    """
    Transcribe an audio file and save the transcript to a text file.

    :param input_filename: Path to the input audio file
    :param output_filename: Path to save the transcript (default: "transcript.txt")
    :param api_key: Groq API key (if None, will attempt to load from environment)
    :return: Execution time in seconds
    """
    # Load API key from environment if not provided
    api_key = None
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")

    if api_key is None:
        logger.error("No API key provided and couldn't load from environment")
        raise ValueError("No API key provided and couldn't load from environment")

    client = Groq(api_key=api_key)

    logger.info("Transcribing audio...")
    start_time = time.time()
    with open(input_filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(input_filename, file.read()),
            model="whisper-large-v3",
            response_format="json",
            language="en",
        )
    execution_time = time.time() - start_time
    logger.info(f"Execution time: {execution_time:.2f} seconds")
    logger.info("Transcription completed.")

    return transcription.text


if __name__ == "__main__":
    print(
        transcribe_audio(
            "data/audio/graphrag-ollama-100-local-setup-keeping-your-data-private_20240804_004855.mp3"
        )
    )
