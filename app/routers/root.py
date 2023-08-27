from fastapi import APIRouter

from app.internal import infra_logger

router_v1 = APIRouter(prefix='/v1')


@router_v1.get("/")
async def get_root():
    """Root GET api endpoint

    Returns:
        "I'm Alive" message
    """

    infra_logger.log_debug("Calling root API - debug")
    infra_logger.log_info("Calling root API")
    return {"message": "I'm Alive"}
