import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))

from youtube_audio_transcriber import download_youtube_audio, transcribe_audio
from client import client
import json
from typing import List, Dict

from utils import SYSTEM_PROMPT_NOTE_GEN, user_prompt_note_gen, MODEL_LLAMA_3_1_405B

from custom_logger import logger

def set_final_prompt(system_prompt: str, user_prompt: str):
    final_prompt = f"""
    <<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {user_prompt}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""
    return final_prompt


def set_payload(prompt, max_gen_len, temperature, top_p):
    payload = {
        "prompt": prompt,
        "max_gen_len": max_gen_len,
        "temperature": temperature,
        "top_p": top_p,
    }
    return payload


def invoke_model_llama_stream(
    client,
    system_prompt: str,
    user_prompt: str,
    model_id,
    max_gen_len=300,
    temperature=0.1,
    top_p=0.9,
):
    final_prompt = set_final_prompt(
        system_prompt=system_prompt, user_prompt=user_prompt
    )
    payload = set_payload(final_prompt, max_gen_len, temperature, top_p)
    body = json.dumps(payload)
    model_id = model_id
    logger.info(f"Model that is used: {model_id}")
    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
    )
    stream = response.get("body")
    for event in stream:
        chunk = event.get("chunk")
        if chunk:
            yield json.loads(chunk.get("bytes").decode())["generation"]


def youtube_transcriber(link: str):
    audio_path = download_youtube_audio(dir_path="data/audio", url=link)
    text_transcript = transcribe_audio(input_filename=audio_path)
    os.remove(audio_path)
    return text_transcript


if __name__ == "__main__":
    text_transcript = youtube_transcriber("https://youtu.be/R6929gi-KwM")
    user_prompt = user_prompt_note_gen(text_transcript)
    for chunk in invoke_model_llama_stream(
            client=client,
            system_prompt=SYSTEM_PROMPT_NOTE_GEN,
            user_prompt=user_prompt,
            model_id=MODEL_LLAMA_3_1_405B,
            max_gen_len=512
        ):
        print(chunk, end="")
