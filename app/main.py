from fastapi import FastAPI
import uvicorn

from app.internal.consts import API_PREFIX, DEBUG_PORT, PROJECT_NAME, VERSION
from app.internal import infra_logger
from app.routers import example, root
from app.routers.chat import chatapi, indexed_chat_api

app = FastAPI()

logger = infra_logger.init_logger()
infra_logger.log_info(
    f"Logger init completed, Log level: {infra_logger.get_current_log_level()}."
)

app = FastAPI(title=PROJECT_NAME, version=VERSION)
app.include_router(example.router_v1, prefix=API_PREFIX)
app.include_router(root.router_v1, prefix=API_PREFIX)
app.include_router(chatapi.router_v1, prefix=API_PREFIX)
app.include_router(indexed_chat_api.router_v1, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=DEBUG_PORT)
