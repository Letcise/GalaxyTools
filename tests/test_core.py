from GalaxyTools import get_logger
from GalaxyTools import initialize_environment
import os

logger= get_logger(__name__)
logger.info("GalaxyTools库初始化.")


initialize_environment()
logger.info(f"项目名{os.getenv('PROJECT_NAME')}")