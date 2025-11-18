import logging
import os

# todo: 1. 添加日志轮转功能 2.根据生产和开发环境配置不同的console_handler


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
    console_handler.setLevel(logging.DEBUG)
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
        info_file_handler = logging.FileHandler(os.path.join(os.getcwd(),log_dir,'info.log'), encoding='utf-8')
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(LevelFilter(logging.INFO))
        info_file_handler.setFormatter(format)
        logger.addHandler(info_file_handler)
    
    def add_error_handler():
        error_file_handler = logging.FileHandler(os.path.join(os.getcwd(),log_dir,'error.log'), encoding='utf-8')
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.addFilter(LevelFilter(logging.ERROR))
        error_file_handler.setFormatter(format)
        logger.addHandler(error_file_handler)
    
    add_info_handler()
    add_error_handler()

def create_logger(name: str = __name__,  log_dir: str = None) -> logging.Logger:
    """
    创建并配置一个 logger 实例。

    参数:
        name (str): logger 的名称，默认为调用模块的 __name__。
        log_dir (str): 日志文件的路径。如果未提供，则默认为 './logs/'。

    返回:
        logging.Logger: 配置好的 logger 实例。
    """
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
    return logger