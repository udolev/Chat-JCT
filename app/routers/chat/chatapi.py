import fastapi
from fastapi import APIRouter

from app.internal.exceptions import LLMChatBasicException
from app.routers.chat.llmcom import get_completion_from_message
from app.routers.chat.models.query_model import Query

from app.internal import infra_logger

router_v1 = APIRouter(prefix='/v1')


@router_v1.post("/chat/user_qeury")
def send_user_qeury(query: Query):
    """
    This is a POST request which generates a new prompt in some llm engine
    and return the response as a JSON.\n
    POST budy contains a json with the next attributes:\n
    context - prompt(s) of the query,\n
    temperature - prompt's temperature parameter (to control creativity),\n 
    llm_engine - wanted llm engine (e.g. openAI),\n
    model - the model of the engine.
    """
    infra_logger.log_info("Received message from the user")
    infra_logger.log_debug(f"Query: {query}")
    try:

        response = get_completion_from_message(query)

        infra_logger.log_info("Received response from FastAPI")
        infra_logger.log_debug(f"{response=}")
        return {"response": response}

    except LLMChatBasicException as ex:
        infra_logger.log_error(
            error_code_recevied=ex.http_code,
            error_text=f"Error calling user-query | {__name__} | {ex}")
        raise fastapi.HTTPException(status_code=ex.http_code, detail=str(ex))
