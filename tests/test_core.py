from GalaxyTools import get_logger
from GalaxyTools import initialize_environment, random_string, call_dify
import os

logger= get_logger(__name__)
logger.info("GalaxyTools库初始化.")

initialize_environment()
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