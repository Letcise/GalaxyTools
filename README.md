# GalaxyTools

A amazing tool for restful api development


## 日志功能

logger默认具备三个handler：console_handler info_file_handler error_file_handler

```python
from GalaxyTools import get_logger
from GalaxyTools import initialize_environment
import os

logger= get_logger(__name__)
logger.info("GalaxyTools库初始化.")


initialize_environment()
logger.info(f"项目名{os.getenv('PROJECT_NAME')}")
