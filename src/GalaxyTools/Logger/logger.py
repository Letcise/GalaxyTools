import logging
import os
import datetime 
from logging.handlers import TimedRotatingFileHandler

_SETUP_DONE = False

class LevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level  # 严格等于该级别

def add_console_handler(logger: logging.Logger, format: logging.Formatter = None) -> None:
    """
    为给定的 logger 添加一个控制台处理器。

    参数:
        logger (logging.Logger): 需要添加控制台处理器的 logger 实例。
        format (logging.Formatter): 用于格式化日志消息的格式化器。
    """
    console_handler = logging.StreamHandler() 
    console_handler.setLevel(logging.INFO)
    if not format:
        format = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    console_handler.setFormatter(format)
    logger.addHandler(console_handler)

def add_file_handler(logger: logging.Logger, log_dir: str = None, format: logging.Formatter = None) -> None:
    """
    为给定的 logger 添加一个文件处理器。

    参数:
        logger (logging.Logger): 需要添加文件处理器的 logger 实例。
        log_dir (str): 日志文件的路径。如果未提供，则默认为 './logs/info.log'和'./logs/error.log'。
        format (logging.Formatter): 用于格式化日志消息的格式化器。
    """
    if not format:
        format = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    def add_info_handler():
        info_file_handler = TimedRotatingFileHandler(
            os.path.join(log_dir,'info.log'), 
            when='midnight',
            interval=1,
            backupCount=7,
            utc=False,
            encoding='utf-8'
        )
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(LevelFilter(logging.INFO))
        info_file_handler.setFormatter(format)
        logger.addHandler(info_file_handler)
    
    def add_error_handler():
        error_file_handler = TimedRotatingFileHandler(
            os.path.join(log_dir,'error.log'), 
            when='midnight',
            interval=1,
            backupCount=7,
            utc=False,
            encoding='utf-8'
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.addFilter(LevelFilter(logging.ERROR))
        error_file_handler.setFormatter(format)
        logger.addHandler(error_file_handler)
    
    add_info_handler()
    add_error_handler()

def setup_logger(name: str,log_dir: str = None) -> None:
    """
    设置全局 logger 。

    参数:
        name (str): 日志名
        log_dir (str): 日志文件的路径。如果未提供，则默认为 './logs/'。
    """
    global _SETUP_DONE
    if _SETUP_DONE:
        return
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    format = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    add_console_handler(logger, format)
    if not log_dir:
        log_dir = './logs'
    os.makedirs(log_dir, exist_ok=True)
    add_file_handler(logger, log_dir, format)
    _SETUP_DONE = True
