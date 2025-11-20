def initialize_environment(env_file: str = ".env"):
    """
    默认从.env文件中加载环境变量.

    参数:
        env_file (str): 环境配置文件名（默认为.env）。
    """
    from dotenv import load_dotenv
    from pathlib import Path
    import os
    file_path = Path(os.getcwd()) / env_file
    if not file_path.exists():
        raise FileNotFoundError(f"指定的环境配置文件不存在: {file_path}")
    if env_file.startswith(".env"):
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv(f".env.{env_file}")

def call_dify(endpoint: str, payload: dict, headers: dict):
    """
    调用Dify API.

    参数:
        endpoint (str): Dify API端点。
        payload (dict): 发送到API的负载数据。
    返回:
        Generator[str]每次 yield 一个data:{}格式数据
    """
    import requests
    with requests.post(endpoint, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()  # 抛出 HTTP 错误
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk and chunk.startswith("data:"):  # 跳过空行（如 SSE 中的 keep-alive 空行）
                yield chunk[5:].strip()  # 移除 "data:" 前缀并去除多余空白

def random_string(length: int = 8) -> str:
    """
    生成指定长度的随机字符串.

    参数:
        length (int): 随机字符串的长度（默认为8）。
    返回:
        str: 生成的随机字符串。
    """
    import random
    import string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

