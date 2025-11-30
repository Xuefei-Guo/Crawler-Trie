from .utils import get_links, get_text, fetch_html, ALLOWED_DOMAINS
from .trie import Trie
import re
import asyncio
import httpx
    

async def crawl_site(start_url: str, max_depth: int, client: httpx.AsyncClient, visited: set[str]| None = None) -> dict[str, list[str]]:
    """
    Given a starting URL, return a mapping of URLs mapped to words that appeared on that page.·

    Parameters:
        start_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.
                    Links from the start page would be depth=1, links from those depth=2, and so on.
        client    - httpx.AsyncClient for making requests.
        visited   - Set of visited URLs to prevent loops.

    Returns:
        Dictionary mapping strings to lists of strings.
        Dictionary keys: URLs of pages visited.
        Dictionary values: lists of all words that appeared on a given page.
    """
    if visited is None:
        visited = set()

    if start_url in visited:
        return {}
    visited.add(start_url)

    try:
        # fetch HTML from starting URL
        html = await fetch_html(client, start_url)
    except Exception:
        # if fetch fails (Already visited or link not allowed), return empty dict
        return {}
    
    # extract words from HTML using regex
    result = {start_url: re.findall(r'[a-zA-Z]+', get_text(html))}
    # if max depth is 0, return only the starting page
    if max_depth <= 0:
        print(f"Crawled: {start_url}")
        return result
    
    links = get_links(html, start_url)
    tasks = []
    for link in links:
        if link.startswith(ALLOWED_DOMAINS) and link not in visited:
            # recursively crawl linked page with decremented depth
            tasks.append(crawl_site(link, max_depth - 1, client, visited))
    
    if tasks:
        sub_results = await asyncio.gather(*tasks)
        _merge_results(result, sub_results)
    return result


def _merge_results(main_result: dict[str, list[str]], sub_results: list[dict[str, list[str]]]):
    """Helper to merge sub-crawl results into the main result."""
    for sub_result in sub_results:
        for url, words in sub_result.items():
            if url not in main_result:
                main_result[url] = words


async def build_index_async(site_url: str, max_depth: int) -> Trie:
    """
    Given a starting URL, build a `Trie` of all words seen mapped to
    the page(s) they appeared upon.

    Parameters:
        site_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.

    Returns:
        `Trie` where the keys are words seen on the crawl, and the
        value associated with each key is a set of URLs that word
        appeared on.
    """
    t = Trie()
    async with httpx.AsyncClient() as client:
        # crawl the site to get mapping of URLs to words
        site_data = await crawl_site(site_url, max_depth, client)
    
    for url, words in site_data.items():
        for word in words:
            try:
                # try to get existing set of URLs for the word
                url_set = t[word]
            except KeyError:
                # if word not in trie, create new set
                url_set = set()
            except Exception:
                continue
            
            # add current URL to the set
            url_set.add(url)
            # store updated set back in trie
            t[word] = url_set
    return t


def build_index(site_url: str, max_depth: int) -> Trie:
    """
    Synchronous wrapper for build_index_async.
    """
    return asyncio.run(build_index_async(site_url, max_depth))
