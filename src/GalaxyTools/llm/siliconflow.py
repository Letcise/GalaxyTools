import os
import requests
import json

"""
data = {
    "model": "Qwen/QwQ-32B",
    "messages": [
        {
            "role": "user",
            "content": "What opportunities and challenges will the Chinese large model industry face in 2025?"
        }
    ],
    "stream": False,
    "max_tokens": 4096,
    "enable_thinking": False,
    "thinking_budget": 4096,
    "min_p": 0.05,
    "stop": None,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": { "type": "text" },
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "<string>",
                "name": "<string>",
                "parameters": {},
                "strict": False
            }
        }
    ]
}
"""

def process_line(line):
    if line.startswith("data"):
        content = line[5:].strip()
        try:
            line_data = json.loads(content)
            think = line_data.get('choices', '')[0].get("delta", "").get('think', '')
            answer = line_data.get('choices', '')[0].get("delta", "").get('content', '')
            return think,answer
        except json.JSONDecodeError as json_e:
            pass
    return  "",""

def process_lines(lines):
    think = ''
    answer = ''
    for line in lines:
        line = line.strip()
        if not line:
            continue
        t,a = process_line(line)
        think += t
        answer += a
    return think,answer

def siliconflow_invoke(data):
    url = os.getenv("SILICONFLOW_ENDPOINT_URL",'https://api.siliconflow.cn/v1/chat/completions')
    token = os.getenv('SILICONFLOW_TOKEN')
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    think = ""
    answer = ""
    response = requests.post(url, json=data, headers=headers, stream=True)
    response.raise_for_status()
    buffer = ''
    for chunk in response.iter_content(chunk_size=128):
        if not chunk:
            continue
        chunk_event = chunk.decode('utf-8', 'replace')
        buffer += chunk_event

        lines = buffer.split('\n')
        t, a = process_lines(lines[:-1])
        think += t
        answer += a
        buffer = lines[-1]

    if buffer.strip():
        lines = buffer.split('\n')
        t, a =  process_lines(lines)
        think += t
        answer += a

    return think,answer
  