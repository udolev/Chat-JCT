# pylint: disable=missing-class-docstring


class LLMChatBasicException(Exception):

    def __init__(self, message, http_code):
        super().__init__(message)
        self.http_code = http_code


class LLMChatAPIERROR(LLMChatBasicException):
    pass


class LLMChatUnsupportedEngine(LLMChatBasicException):
    pass


class LLMChatUnknownError(LLMChatBasicException):
    pass


class LLMChatTimeoutError(LLMChatBasicException):
    pass


class LLMChatAPIConnectionError(LLMChatBasicException):
    pass


class LLMChatInvalidRequestError(LLMChatBasicException):
    pass


class LLMChatAuthenticationError(LLMChatBasicException):
    pass


class LLMChatPermissionError(LLMChatBasicException):
    pass


class LLMChatRateLimitError(LLMChatBasicException):
    pass


class LLMChatServiceUnavailableError(LLMChatBasicException):
    pass


class LLMChatStorageNotFound(LLMChatBasicException):
    pass
