from dotenv import load_dotenv
from pathlib import Path
import os

def initialize_environment(env_file: str = ".env"):
    """
    默认从.env文件中加载环境变量.

    参数:
        env_file (str): 环境配置文件名（默认为.env）。
    """
    file_path = Path(os.getcwd()) / env_file
    if not file_path.exists():
        raise FileNotFoundError(f"指定的环境配置文件不存在: {file_path}")
    if env_file.startswith(".env"):
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv(f".env.{env_file}")

