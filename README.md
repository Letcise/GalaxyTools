# GalaxyTools

A amazing tool for restful api development

## 源码使用说明

安装源码
```bash
# 使用 pip
pip install -e .
# 使用uv
uv pip install -e .

### 日志功能

logger默认具备三个handler：console_handler info_file_handler error_file_handler

```python
from GalaxyTools import get_logger
import os

logger= get_logger()
logger.info("GalaxyTools库初始化.")
```

### 工具功能


```python
from GalaxyTools import get_logger
from GalaxyTools import initialize_environment, random_string, call_dify, map_folder, 
import os
initialize_environment()
logger= get_logger(__name__)
logger.info(f"项目名{os.getenv('PROJECT_NAME')}")
print(random_string(10))
chunks = call_dify(
    endpoint=os.getenv("DIFY_ENDPOINT") + '/chat-messages',
    payload={
        "inputs": {},
        "query": "你好",
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "abc-123",
        "files": []
    },
    headers={
        'Content-Type':'application/json',
        'Authorization': f'Bearer {os.getenv("DIFY_API_KEY")}'
    }
)
for chunk in chunks:
    print(chunk)

logger = get_logger()

def read_text(file, use_logger = False):
    f = open(file, encoding='utf-8')
    text = f.read()
    f.close()
    if use_logger:
        logger.info(text)
    else:
        print(text)
    return text

print(
    map_folder(
        read_text,
        './doc',
        use_logger = True
    )
)
```

### LLM 调用

```python
from GalaxyTools import openai_invoke, siliconflow_invoke
# 使用siliconflow_invoke前配置SILICONFLOW_ENDPOINT_URL SILICONFLOW_TOKEN环境变量
# 使用openai_invoke前配置OPENAI_API_KEY OPENAI_ENDPOINT_URL环境变量

# 传入data参数
think, answer = siliconflow_invoke(data)
think, answer = openai_invoke(data)

```
