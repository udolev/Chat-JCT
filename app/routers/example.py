from fastapi import APIRouter

from app.internal import infra_logger

router_v1 = APIRouter(prefix='/v1')


@router_v1.get("/simple")
async def get_simple():
    """Simple GET api endpoint

    Returns:
        Just hello world
    """

    infra_logger.log_debug("Calling simple API - debug")
    infra_logger.log_info("Calling simple API")
    return {"message": "Hello World"}
