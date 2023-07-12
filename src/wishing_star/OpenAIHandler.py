import logging
import openai
from typing import Any, Dict, Optional
from wishing_star.utils import get_current_ts


class OpenAIHandler:
    """
    This class implements the handlers to response to OpenAI related requests.
    """

    def __init__(self, api_key: str, logger: logging.Logger):
        """
        Initializes the handler.

        :param self
        :param api_key: API Key generated by Open AI.
        :param logger: Global logger passed into the handler.
        """
        openai.api_key = api_key
        self.logger: logging.Logger = logger
        self.last_success_request_ts: int = 0
        self.minimum_request_period: int = 15 * 1000  # 15 seconds
        self.model: str = "gpt-3.5-turbo"
        self.last_response: Optional[str] = None

    def chat(self, msg: str, user_id: int) -> str:
        """
        Sends the chat to the gpt and returns the response.

        TODO: cache the last few dialog to make the chat complete.
        :param self
        :param msg: Input message from the user.
        :param user_id: Discord user id.
        :return: The response.
        :raise RequestRateException if the access is too frequent.
        """
        if get_current_ts() - self.last_success_request_ts <= self.minimum_request_period:
            return "T.T Jirachi gets too many questions and needs some time to rest..."

        msg = "brief answer:" + msg
        self.logger.info(
            f"Initiates OpenAI Chat Request from User ID: {user_id}. Message content:\n{msg}"
        )
        response: Dict[Any, Any] = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "user", "content": msg},
            ],
        )
        self.last_response = response["choices"][0]["message"]["content"]
        prompt_tokens: int = response["usage"]["prompt_tokens"]
        completion_tokens: int = response["usage"]["completion_tokens"]

        self.logger.info(
            f"OpenAI Chat Request Complete. #Prompt tokens: {prompt_tokens}; #Completion tokens:"
            f" {completion_tokens}. Response:\n{self.last_response}"
        )
        if None is self.last_response:
            raise Exception("None Response received from OpenAI Chat Request.")
        self.last_success_request_ts = get_current_ts()
        return self.last_response