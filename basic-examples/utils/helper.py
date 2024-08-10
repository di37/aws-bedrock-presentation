import os, sys
from os.path import dirname as up

sys.path.append(os.path.abspath(os.path.join(up(__file__), os.pardir)))
import json

from client import client
from utils import SYSTEM_PROMPT_LLAMA, MODEL_LLAMA_3_1_405B
from typing import List, Dict

from custom_logger import logger

## Prompt template source: https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1


def set_final_prompt(prompt):
    final_prompt = f"""
    <<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{SYSTEM_PROMPT_LLAMA}<|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {prompt}<|eot_id|>
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


def invoke_model_llama(
    prompt,
    model_id,
    max_gen_len=300,
    temperature=0.1,
    top_p=0.9,
):
    final_prompt = set_final_prompt(prompt)
    payload = set_payload(final_prompt, max_gen_len, temperature, top_p)
    body = json.dumps(payload)
    model_id = model_id
    logger.info(f"Model used: {model_id}")
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    repsonse_text = response_body["generation"]
    return repsonse_text


def invoke_model_llama_stream(
    prompt,
    model_id,
    max_gen_len=300,
    temperature=0.1,
    top_p=0.9,
):
    final_prompt = set_final_prompt(prompt)
    payload = set_payload(final_prompt, max_gen_len, temperature, top_p)
    body = json.dumps(payload)
    model_id = model_id
    logger.info(f"Model used: {model_id}")
    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
    )
    stream = response.get("body")
    for event in stream:
        chunk = event.get("chunk")
        if chunk:
            yield json.loads(chunk.get("bytes").decode())["generation"]


def converse_llama(
    bedrock_client,
    model_id: str,
    system_prompts: List[Dict[str, str]],
    messages: List[Dict[str, List[Dict[str, str]]]],
    max_gen_len: int = 512,
    temperature: float = 0.5,
    top_p: float = 0.9,
) -> Dict:
    """
    Sends messages to a model and returns the response.
    """

    inference_config = {"temperature": temperature}
    additional_model_fields = {"top_p": top_p, "max_gen_len": max_gen_len}
    logger.info(f"Model used: {model_id}")
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
    )

    return response


def converse_llama_stream(
    bedrock_client,
    model_id: str,
    system_prompts: List[Dict[str, str]],
    messages: List[Dict[str, List[Dict[str, str]]]],
    max_gen_len: int = 512,
    temperature: float = 0.5,
    top_p: float = 0.9,
):
    """
    Sends messages to a model and returns the response.
    """

    inference_config = {"temperature": temperature}
    additional_model_fields = {"top_p": top_p, "max_gen_len": max_gen_len}
    logger.info(f"Model used: {model_id}")
    response = bedrock_client.converse_stream(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
    )

    stream = response.get("stream")
    if stream:
        for event in stream:

            # if "messageStart" in event:
            #     print(f"\nRole: {event['messageStart']['role']}")

            if "contentBlockDelta" in event:
                # print(event["contentBlockDelta"]["delta"]["text"], end="")
                yield event["contentBlockDelta"]["delta"]["text"]

            # if "messageStop" in event:
            #     print(f"\nStop reason: {event['messageStop']['stopReason']}")

            # if "metadata" in event:
            #     metadata = event["metadata"]
            #     if "usage" in metadata:
            #         print("\nToken usage")
            #         print(f"Input tokens: {metadata['usage']['inputTokens']}")
            #         print(f":Output tokens: {metadata['usage']['outputTokens']}")
            #         print(f":Total tokens: {metadata['usage']['totalTokens']}")
            #     if "metrics" in event["metadata"]:
            #         print(f"Latency: {metadata['metrics']['latencyMs']} milliseconds")


if __name__ == "__main__":
    system_prompt = "You are a helpful assistant. Provide concise and accurate responses to user queries."
    messages = []
    messages.append(
        {
            "role": "user",
            "content": [{"text": "Explain the difference between a cat and a dog."}],
        }
    )
    print(
        converse_llama_stream(
            bedrock_client=client,
            model_id=MODEL_LLAMA_3_1_405B,
            system_prompts=[{"text": system_prompt}],
            messages=messages,
        )
    )
