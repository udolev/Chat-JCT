import http
import fastapi
from fastapi import APIRouter

from app.internal.exceptions import LLMChatBasicException
from app.routers.chat.llama_index_com import get_completion_from_message_with_indexing
from app.routers.chat.models.indexed_query_model import IndexedQuery

from app.internal import infra_logger

router_v1 = APIRouter(prefix='/v1')


@router_v1.post("/chat/special_assistant")
def send_indexed_qeury(query: IndexedQuery):
    """
    This is a POST request which generates a new prompt in some llm engine
    with indexing and returns the response as a JSON.\n
    POST budy contains a json with the next attributes:\n
    prompt - prompt of the query,\n
    temperature - prompt's temperature parameter (to control creativity),\n 
    llm_engine - wanted llm engine (e.g. openAI),\n
    model - the model of the engine, \n
    llm_context - the wanted context files.
    """
    infra_logger.log_info("Received message from the user in indexed chat API")
    infra_logger.log_debug(f"Index Query: {query.dict()}")
    try:

        response = get_completion_from_message_with_indexing(query)
        infra_logger.log_info("Received response from indexed chat API")
        infra_logger.log_debug(f"{response=}")
        return {"response": response}

    except LLMChatBasicException as ex:
        infra_logger.log_error(
            error_code_recevied=ex.http_code,
            error_text=f"Error calling indexed-query | {__name__} | {ex}")
        raise fastapi.HTTPException(status_code=ex.http_code, detail=str(ex))

    except Exception as ex:
        infra_logger.log_error(
            error_code_recevied=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            error_text=f"Error calling indexed-query | {__name__} | {ex}")
        raise fastapi.HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(ex))
