import os
from abc import abstractmethod
from typing import Protocol
from http import HTTPStatus

import openai
from openai.error import (APIError, Timeout, APIConnectionError,
                          InvalidRequestError, AuthenticationError,
                          PermissionError as OpenAiPermissionsError,
                          RateLimitError, ServiceUnavailableError)

from app.internal.exceptions import LLMChatAuthenticationError, LLMChatAPIERROR, LLMChatAPIConnectionError, LLMChatInvalidRequestError, \
    LLMChatRateLimitError, LLMChatServiceUnavailableError, LLMChatPermissionError, LLMChatTimeoutError, LLMChatUnknownError, \
    LLMChatUnsupportedEngine
from app.routers.chat.models.query_model import Query, LlmEngine
from app.internal.consts import OPENAI_API_KEY_ENV
from app.internal import infra_logger


class BaseLLMEngine(Protocol):
    '''Base class to represent llm engins'''

    @abstractmethod
    def get_completion_from_message(self):
        raise NotImplementedError


class OpenAIEngine(BaseLLMEngine):
    '''Simple class to handle OpenAI communication'''

    def __init__(self, query: Query):
        try:
            openai.api_key = os.environ[OPENAI_API_KEY_ENV]
        except APIError as ex:
            raise LLMChatAPIERROR(
                "API error", http_code=HTTPStatus.SERVICE_UNAVAILABLE) from ex
        except APIConnectionError as ex:
            raise LLMChatAPIConnectionError(
                "error while connecting with the API",
                http_code=HTTPStatus.INTERNAL_SERVER_ERROR) from ex
        self.query = query
        infra_logger.log_info("Initiated openAI llm engine")
        infra_logger.log_debug(f"chat query: {query.dict()}")

    def get_completion_from_message(self):
        '''The function gets a prompt and sends it to openai with relevant context.
        Then, it returns the answer'''
        try:
            response = openai.ChatCompletion.create(
                model=self.query.model,
                messages=self.query.dict()['context'],
                temperature=self.query.temperature,
            )
            infra_logger.log_info("Received response from openAI")
            infra_logger.log_debug(
                f'openAI response: {response.choices[0].message["content"]}')
            return response.choices[0].message["content"]
        except InvalidRequestError as ex:
            infra_logger.log_debug(f'caught exception: {ex}, {type(ex)}')
            raise LLMChatInvalidRequestError(
                "Invalid Request Error",
                http_code=HTTPStatus.BAD_REQUEST) from ex
        except RateLimitError as ex:
            infra_logger.log_debug(f'caught exception: {ex}, {type(ex)}')
            raise LLMChatRateLimitError(
                "Rate limit error",
                http_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE) from ex
        except ServiceUnavailableError as ex:
            infra_logger.log_debug(f'caught exception: {ex}, {type(ex)}')
            raise LLMChatServiceUnavailableError(
                "OpenAI service is unavailable",
                http_code=HTTPStatus.SERVICE_UNAVAILABLE) from ex
        except AuthenticationError as ex:
            infra_logger.log_debug(f'caught exception: {ex}, {type(ex)}')
            raise LLMChatAuthenticationError(
                "Authentication error occurred",
                http_code=HTTPStatus.UNAUTHORIZED) from ex
        except OpenAiPermissionsError as ex:
            infra_logger.log_debug(f'caught exception: {ex}, {type(ex)}')
            raise LLMChatPermissionError(
                "Permission error", http_code=HTTPStatus.FORBIDDEN) from ex
        except Timeout as ex:
            raise LLMChatTimeoutError(
                "Timeout error", http_code=HTTPStatus.REQUEST_TIMEOUT) from ex
        except Exception as ex:  # pylint: disable=broad-exception-raised
            infra_logger.log_debug(
                f'caught unknown exception: {ex}, {type(ex)}')
            raise LLMChatUnknownError(
                "Unknown error has occurred",
                http_code=HTTPStatus.INTERNAL_SERVER_ERROR) from ex


def get_completion_from_message(query: Query):
    '''The function gets a prompt and sends it to the appropriate llm completion function'''
    infra_logger.log_debug('In get_completion_from_message function')
    if query.llm_engine == LlmEngine.OPEN_AI:
        engine = OpenAIEngine(query)
        return engine.get_completion_from_message()
    raise LLMChatUnsupportedEngine(
        f"Chat doesn't support llm engine: {query.llm_engine}",
        http_code=HTTPStatus.METHOD_NOT_ALLOWED)
