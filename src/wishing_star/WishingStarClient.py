import discord
import logging
from typing import Any, Dict, Optional
from wishing_star.OpenAIHandler import OpenAIHandler


class WishingStarClient(discord.Client):
    """
    This class is a derived class of discord.Client.

    It should define all the functions that response to the received requests.
    """

    def __init__(
        self, intents: discord.Intents, logger: logging.Logger, credential: Dict[str, Any]
    ):
        """
        Initializes the client with customized data members.

        :param intents: Arguments passed into the parent class.
        :param logger: Logging handler.
        :param credential: A dictionary that contains necessary credential keys.
        """
        super().__init__(intents=intents)
        self.logger: logging.Logger = logger
        self.discord_key: str = credential["discord_key"]
        self.openai_handler: OpenAIHandler = OpenAIHandler(credential["openai_key"], logger)

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
        if src_message.startswith("?q:"):
            try:
                response: str = self.openai_handler.chat(src_message[3:], src_id)
                await message.reply(response, mention_author=True)
            except Exception as e:
                self.logger.warning(e)
