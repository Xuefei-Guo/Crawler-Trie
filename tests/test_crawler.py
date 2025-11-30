import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from trie_search.crawler import crawl_site, build_index_async

@pytest.mark.asyncio
async def test_crawl_site():
    # Mock httpx client
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.text = '<html><body><a href="https://example.com/page1">link</a><p>hello world</p></body></html>'
    mock_client.get.return_value = mock_response
    
    # Mock utils functions to avoid actual parsing logic dependency if needed, 
    # but here we can rely on the actual utils if they are pure functions.
    # However, get_links and get_text use lxml, so let's mock them for isolation or just let them run.
    # Let's mock fetch_html to avoid network calls, which we already did by mocking client.
    
    # We need to patch fetch_html in crawler.py because it's imported there
    with patch('trie_search.crawler.fetch_html', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = '<html><body><a href="https://example.com/page1">link</a><p>hello world</p></body></html>'
        
        # We also need to mock get_links to return controlled links
        with patch('trie_search.crawler.get_links') as mock_get_links:
            mock_get_links.return_value = ["https://example.com/page1"]
            
            # Mock get_text
            with patch('trie_search.crawler.get_text') as mock_get_text:
                mock_get_text.return_value = "hello world"
                
                start_url = "https://example.com"
                result = await crawl_site(start_url, 1, mock_client)
                
                assert start_url in result
                assert "hello" in result[start_url]
                assert "world" in result[start_url]
                # Since depth is 1, it should crawl the start page and its links (depth 0 for links)
                # Wait, depth 1 means start page (depth 1) -> links (depth 0). 
                # The code says: recursively crawl linked page with decremented depth.
                # If max_depth <= 0, return.
                # So call(1) -> process start -> call(0) for links -> process links -> call(-1) -> return.
                
                assert "https://example.com/page1" in result

