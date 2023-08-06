from ..base import BaseShortener
from ..exceptions import ShorteningErrorException, ExpandingErrorException


class Shortener(BaseShortener):
    """
    cloudflare page shortener implementation

    Example:

        >>> import pydlj
        >>> s = pydlj.Shortener()
        >>> s.cf.short('http://www.google.com')
    """

    api_url = "https://bitly.ddot.cc/"

    def short(self, url):
        """Short implementation for Da.gd
        Args:
            url (str): the URL you want to shorten

        Returns:
            str: The shortened URL.

        Raises:
            ShorteningErrorException: If the API Returns an error as response
        """
        url = self.clean_url(url)
        shorten_url = f"{self.api_url}"
        response = self._post(shorten_url, json={"url": url})
        if not response.ok:
            raise ShorteningErrorException(response.content)
        return response.json()["url"].strip()

    def expand(self, url):
        """Expand implementation for Da.gd
        Args:
            url (str): The URL you want to expand.

        Returns:
            str: The expanded URL.

        Raises:
            ExpandingErrorException: If the API Returns an error as response.
        """

        url = self.clean_url(url)
        # da.gd's coshorten expects only the shorturl identifier
        # (i.e. the "stuff" in http://da.gd/stuff), not the full short URL.
        expand_url = url
        response = self._get(expand_url)
        if not response.ok:
            raise ExpandingErrorException(response.content)
        return response.text.strip()
