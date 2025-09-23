from typing import List
from googleapiclient.discovery import build

from internal.clients.search import SearchClient


class GoogleSearchClient(SearchClient):
    """The GoogleSearchClient performs Google searches."""

    def __init__(self, engine_id: str, api_key: str) -> None:
        """
        Initialise the GoogleSearchClient class

        Args:
            engine_id: The id of the custom search engine to use
            api_key: The developer API key used in searches
        """
        self.__engine_id = engine_id
        self.__service = build("customsearch", "v1", developerKey=api_key).cse()

    def list(self, query: str, page: int = 0, page_size: int = 10) -> List[str]:
        """
        Performs a search and lists the URLs with pagination.

        Args:
            query: the search query to use.
            page: the page number to return.
            page_size: the number of items to return per page.

        Returns:
            a list of urls from the response.
        """
        # Search google using the provided query
        try:
            # Note: max page size (num) for this service is 10
            #       and page start + page size (start + num) cannot exceed 100
            response = self.__service.list(
                q=query, cx=self.__engine_id, safe="active", start=page * page_size, num=page_size
            ).execute()
        except Exception as e:
            raise Exception(f"Could not list search results with Google: `{str(e)}`.")

        if not response or "items" not in response.keys() or not response.get("items"):
            return []

        return [item.get("link") for item in response.get("items")]
