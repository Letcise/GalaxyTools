from openai import OpenAI
import os
import json


"""
data = {
    'model':'qwen3-30b-a3b-instruct-2507',
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    'stream':True
}
"""


def openai_client_factory(api_key, base_url):
    client = None
    def construct_client():
        nonlocal client
        if client is None:
            client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )
        return client
    return construct_client


def parsing(data):
    model = data.get('model')
    messages = data.get('messages')
    stream = data.get('stream', True)
    enable_thinking = data.get("enable_thinking", False)
    return model, messages, stream, enable_thinking
    


def openai_invoke(data):
    model, messages, stream, enable_thinking = parsing(data)
    lazy_client = openai_client_factory(
        os.getenv("OPENAI_API_KEY"),
        os.getenv("OPENAI_ENDPOINT_URL"),
    )
    client = lazy_client()
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={"enable_thinking": enable_thinking},
        stream=stream
    )
    think = ""
    answer = ""
    for chunk in completion:
        data = json.loads(chunk.model_dump_json()).get('choices')[0].get('delta')
        think += data.get('reasoning_content','')
        answer += data.get('content','')
    return think, answer
