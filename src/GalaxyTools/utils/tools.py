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

def save_text(file_position : str, content : str) -> bool:
    """
    保存文本文件.

    参数:
        file_position (str): 文本保存的位置。
        content (str): 文本内容。
    返回:
        str: 生成的随机字符串。
    """
    try:
        from pathlib import Path
        path = Path(file_position)
        import os
        env = os.getenv('env', 'development')
        if env != 'production':
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"文件将保存在{path.parent}中")
        path.parent.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return True
    except:
        return False

from typing import Callable, List, Any
import os
def map_folder(func: Callable, folder_path: str, *args, concurrent: int = 1, 
               key: Callable = None, use_thread: bool = True, 
               **kwargs) -> List[Any]:
    """
    对 folder_path 中的每个文件（或子项）调用 func(item_path, *args, **kwargs)

    Args:
        func (Callable): 待调用函数
        folder_path (str): 文件夹路径
        concurrent (int, optional): 并发数。默认为 1（串行）。
        key (Callable, optional): 排序函数。默认为 None（不排序）。
        use_thread (bool, optional): 是否使用线程池。默认为 True（使用线程池）。
        *args: 传递给 func 的其他位置参数
        **kwargs: 传递给 func 的其他关键字参数

    Returns:
        list: 每个文件处理结果形成的列表
    """
    items = os.listdir(folder_path)
    if key:
        items.sort(key=key)
    item_paths = [os.path.join(folder_path, item) for item in items]

    if concurrent == 1:
        return [func(item, *args, **kwargs) for item in item_paths]
    else:
        from .concurrent import ConcurrentMap
        if use_thread:
            return ConcurrentMap.thread_map(func, item_paths, *args, max_workers=concurrent, **kwargs)
        else:
            return ConcurrentMap.process_map(func, item_paths, *args, max_workers=concurrent, **kwargs)

def read_text(file:str, encoding='utf-8') -> str:
    """读取文本文件

    Args:
        file (str): 文件路径
        use_logger (str): 文件编码方式. Defaults to utf-8.

    Returns:
        str: 文本内容
    """
    with open(file, encoding='utf-8') as f:
        return f.read()