from abc import ABC, abstractmethod
from typing import List


class SearchClient(ABC):
    """The SearchClient performs external searches with the internet."""

    @abstractmethod
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
        ...
