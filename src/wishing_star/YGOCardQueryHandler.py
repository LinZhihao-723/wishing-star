import logging
import requests
from typing import Any, Dict, Generator, List


class YGOCardQueryHandler:
    """
    This class handles YGO card search requests.
    """

    search_api_endpoint: str = "https://ygocdb.com/api/v0"
    image_url_endpoint: str = "https://images.ygoprodeck.com/images/cards"

    def __init__(self, logger: logging.Logger):
        """
        Initialize the handler.

        :param self
        :param logger: Global logging handler.
        """
        self.logger: logging.Logger = logger

    def stream_formatted_card_info(self, card_info: Dict[str, Any]) -> str:
        """
        Formats the card information into a string that should be sent back to
        the users.

        :param self
        :param card_info: Dictionary that contains card information. :return
            Formatted card information as a string.
        """
        cn_name: str = card_info["cn_name"]
        jp_name: str = card_info["jp_name"]
        en_name: str = card_info["en_name"]
        card_id: int = card_info["id"]
        types: str = card_info["text"]["types"]
        desc: str = card_info["text"]["desc"]
        img_url: str = f"{YGOCardQueryHandler.image_url_endpoint}/{card_id}.jpg"
        search_result: str = (
            "YGO Card Search Result:\n"
            f"CN Name: {cn_name}\n"
            f"JP Name: {jp_name}\n"
            f"EN Name: {en_name}\n"
            f"Card ID: {card_id}\n"
            f"Types: {types}\n"
            f"Description: {desc}\n"
            f"Image: {img_url}\n"
        )

        return search_result

    def search_query(self, query: str) -> Generator[str, None, None]:
        """
        This is a generator that returns the results one by one that match the
        search query.

        :param self
        :param query: Search query input.
        :yield: A single matched search result on each yield.
        """
        self.logger.info(f'YGO Search Query: "{query}"')
        params: Dict[str, str] = {"search": query}
        response: requests.Response = requests.get(
            YGOCardQueryHandler.search_api_endpoint, params=params
        )
        status_code: int = response.status_code
        if 200 == status_code:
            data: Dict[str, Any] = response.json()
            results: List[Dict[str, Any]] = data["result"]
            self.logger.info(f'YGO Search Query "{query}": {len(results)} results found.')
            for card_info in results:
                yield self.stream_formatted_card_info(card_info)
        else:
            raise Exception(f'YGO Search Query "{query}" failed with status code {status_code}')
