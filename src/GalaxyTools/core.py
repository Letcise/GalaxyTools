from .Logger.logger import create_logger

logger = create_logger(__name__)  # 创建一个模块级别的 logger
logger.info("GalaxyTools core module loaded.")