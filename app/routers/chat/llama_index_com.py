from http import HTTPStatus
import os
from pathlib import Path

from llama_index import StorageContext, load_index_from_storage

from app.routers.chat.models.indexed_query_model import IndexedQuery
from app.internal.exceptions import LLMChatStorageNotFound
from app.internal import infra_logger


def get_completion_from_message_with_indexing(query: IndexedQuery):
    adding_data = AddingDataToLlmEngine(query)
    infra_logger.log_debug(
        debug_text=f"llama response: {adding_data.response}")
    infra_logger.log_info("Received response from llama index")
    return adding_data.response.response


class AddingDataToLlmEngine:
    '''Simple class used for adding data to query'''

    def __init__(self, query: IndexedQuery):
        self.index = None
        self.persist_dir = str(Path(os.getcwd()).joinpath('assistants').joinpath('storage') \
                               .joinpath(query.llama_context))
        self.data_dir = str(Path(os.getcwd()).joinpath('assistants').joinpath('data') \
                            .joinpath(query.llama_context))
        if not os.path.exists(self.persist_dir):
            infra_logger.log_error(error_code_recevied=-1,
                                   error_text="Missing storage file")
            raise LLMChatStorageNotFound(
                http_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message=f"Llama context for {query.llama_context} was not found"
            )
        self.read_from_storage()
        query_engine = self.index.as_query_engine()
        self.response = query_engine.query(query.prompt)

    def read_from_storage(self):
        storage_context = StorageContext.from_defaults(
            persist_dir=self.persist_dir)
        self.index = load_index_from_storage(storage_context=storage_context)
