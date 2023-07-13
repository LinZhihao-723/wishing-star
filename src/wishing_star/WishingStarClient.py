import discord
import logging
from discord.ext import commands
from typing import Any, Dict, Optional, Union
from wishing_star.Exceptions import FrequentRequestRateException
from wishing_star.OpenAIHandler import OpenAIHandler
from wishing_star.YGOCardQueryHandler import YGOCardQueryHandler


class WishingStar(commands.Bot):
    """
    This class is a derived class of discord.commands.Bot.

    This is the top level client that handles all the user inputs and backend
    jobs.
    """

    keyword_openai_handler: str = "Jirachi"
    keyword_ygo_query: str = "?ygo "

    def __init__(
        self,
        command_prefix: Union[str, Any],
        logger: logging.Logger,
        credential: Dict[str, Any],
        **options: Any,
    ):
        """
        Initializes the client with customized data members.

        :param self
        :param command_prefix: The condition when the bot will be triggered by a
            command.
        :param logger: Global logging handler.
        :param credential: A dictionary that contains necessary credential keys.
        :param options: Other options to initialize the low level bot.
        """
        super().__init__(command_prefix, **options)
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

    async def process_jirachi_chatting(self, message: discord.Message, src_id: int) -> None:
        """
        Process the input chat by redirecting the message to the OpenAI backend.

        :param self
        :param message: Discord message that contains the new chat.
        :param src_id: The Discord Id of the message owner. :raise
            FrequentRequestRateException: The chat is too frequent.
        """
        try:
            chat_content: str = message.content
            chat_content = chat_content[chat_content.index(" ") + 1 :]
            response: str = self.openai_handler.chat(chat_content, src_id)
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

    async def on_message(self, message: discord.Message) -> None:
        """
        Override Message handler.

        :param self
        :param message: Discord message received.
        """
        assert None is not self.user
        src_id: Optional[int] = message.author.id

        if None is src_id:
            self.logger.warning(f"On message: Author id not found: {str(message.author)}")
            return

        if src_id == self.user.id:
            return

        if self.user in message.mentions:
            await self.process_jirachi_chatting(message, src_id)
            return

        await self.process_commands(message)


class WishingStarCog(commands.Cog):
    """
    This class contains basic Wishing Star commands.
    """

    def __init__(self, wishing_star: WishingStar):
        """
        Initializes with the wishing star bot.

        :param self
        :param wishing_star: An instance of WishingStar bot.
        """
        self.ws: WishingStar = wishing_star
        self.logger: logging.Logger = wishing_star.logger

    @commands.command()
    async def ygo(
        self,
        context: commands.Context, # type: ignore
        search_query: Optional[str]
    ) -> None:
        """
        Processes YGO search query.
        
        :param self
        :param context: Context input from the users.
        :param search_query: Search input. It is possible to be None.
        """
        try:
            if None is search_query or 0 == len(search_query):
                await context.reply("Empty Query Received.", mention_author=True)
                return
            result_count: int = 0
            for result in self.ws.ygo_query_handler.search_query(search_query):
                await context.reply(result, mention_author=True)
                result_count += 1
            if 0 == result_count:
                await context.reply("No result found.", mention_author=True)
            else:
                await context.reply(
                    f"Query complete. Total results found: {result_count}", mention_author=True
                )
        except Exception as e:
            self.logger.warning(e)
