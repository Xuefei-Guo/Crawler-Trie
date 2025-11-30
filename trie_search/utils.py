"""
Web crawling utilities, do not modify this file.
"""

import httpx
import lxml.html

ALLOWED_DOMAINS = ("https://")


class FetchException(Exception):
    pass


async def fetch_html(client: httpx.AsyncClient, url: str) -> str:
    """
    Fetch HTML from a given URL asynchronously.

    Parameters:
        client - httpx.AsyncClient instance.
        url - URL to fetch.

    Returns:
        String containing HTML from the page.
    """
    if not url.startswith("https://"):
        raise FetchException(f"URL {url} must start with https://")
    elif not url.startswith(ALLOWED_DOMAINS):
        raise FetchException(f"URL {url} does not start with an allowed domain")
    try:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise FetchException(str(e))


def get_links(html: str, source_url: str) -> list[str]:
    """
    Get all URLs that are on a given page.

    Parameters:
        html - Page HTML.
        source_url - URL of source page.

    Returns:
        List of URLs that appeared on page.
    """
    doc = lxml.html.fromstring(html)
    doc.make_links_absolute(source_url)
    return doc.xpath("//a/@href")


def get_text(html: str) -> str:
    """
    Get all text on a given page.

    Parameters:
        html - Page HTML.

    Returns:
        Text extracted from the page.
    """
    return lxml.html.fromstring(html).text_content()
