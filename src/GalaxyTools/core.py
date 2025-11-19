from .Logger.logger import setup_logger
import logging

def get_logger(name=None) -> logging.Logger:
    setup_logger()  # 自动 lazy 初始化
    return logging.getLogger(name or __name__)