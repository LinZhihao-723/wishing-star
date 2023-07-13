import discord
import logging
from typing import Any, Dict, Optional
from wishing_star.Exceptions import FrequentRequestRateException
from wishing_star.OpenAIHandler import OpenAIHandler
from wishing_star.YGOCardQueryHandler import YGOCardQueryHandler


class WishingStarClient(discord.Client):
    """
    This class is a derived class of discord.Client.

    This is the top level client that handles all the user inputs and backend
    jobs.
    """

    keyword_openai_handler: str = "Jirachi"
    keyword_ygo_query: str = "?ygo "

    def __init__(
        self, intents: discord.Intents, logger: logging.Logger, credential: Dict[str, Any]
    ):
        """
        Initializes the client with customized data members.

        :param intents: Arguments passed into the parent class.
        :param logger: Global logging handler.
        :param credential: A dictionary that contains necessary credential keys.
        """
        super().__init__(intents=intents)
        self.logger: logging.Logger = logger
        self.discord_key: str = credential["discord_key"]
        self.openai_handler: OpenAIHandler = OpenAIHandler(credential["openai_key"], logger)
        self.ygo_query_handler: YGOCardQueryHandler = YGOCardQueryHandler(logger)

    def serve(self) -> None:
        """
        Wrapper for self.run.

        :param self
        """
        self.run(self.discord_key)

    async def on_ready(self) -> None:
        assert None is not self.user
        self.logger.info(f"Logged in as <{self.user}> ID: <{self.user.id}>")

    async def on_message(self, message: discord.Message) -> None:
        assert None is not self.user
        src_id: Optional[int] = message.author.id

        if None is src_id:
            self.logger.warning(f"On message: Author id not found: {str(message.author)}")
            return

        if src_id == self.user.id:
            return

        src_message: str = message.content
        if src_message.startswith(WishingStarClient.keyword_openai_handler):
            try:
                response: str = self.openai_handler.chat(
                    src_message[len(self.keyword_openai_handler) :], src_id
                )
                end_pos: int = 0
                response_len: int = len(response)
                while end_pos < response_len:
                    start_pos: int = end_pos
                    end_pos = min(end_pos + 1800, response_len)
                    await message.reply(response[start_pos:end_pos], mention_author=True)
            except FrequentRequestRateException:
                await message.reply(
                    "T.T Jirachi gets too many questions and need to sleep for a while",
                    mention_author=True,
                )
            except Exception as e:
                self.logger.warning(e)

        elif src_message.startswith(WishingStarClient.keyword_ygo_query):
            try:
                search_query: str = src_message[len(WishingStarClient.keyword_ygo_query) :]
                result_count: int = 0
                for result in self.ygo_query_handler.search_query(search_query):
                    await message.reply(result, mention_author=True)
                    result_count += 1
                if 0 == result_count:
                    await message.reply("No result found.", mention_author=True)
                else:
                    await message.reply(
                        f"Query complete. Total results found: {result_count}", mention_author=True
                    )
            except Exception as e:
                self.logger.warning(e)
