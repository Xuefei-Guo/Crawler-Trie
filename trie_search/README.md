# TrieSpider

## Features
- **High Performance**: Asynchronous web crawler using `asyncio` and `httpx` for concurrent fetching.
- **Efficient Search**: Trie-based index supporting wildcard search and autocomplete.
- **User-Friendly Configuration**: Manage start URL and crawl depth directly from the web interface.
- **Containerized**: Docker support for easy deployment.

## How to Run

### Local Development
1. Install dependencies:
   ```zsh
   uv sync
   ```
2. Run the web server:

   Default URL = "https://example.com", Depth = 2:
   ```zsh
   uv run flask --app trie_search.web run
   ```
   Or modify the URL and Depth using env:
   ```zsh
   # MaxOS/Linux
   URL="https://xxxxxxx" DEPTH=x uv run flask --app trie_search.web run

   # Windows
   $env:URL="https://xxxxxxx"; $env:DEPTH=x; uv run flask --app trie_search.web run
   ```
   
   *Note: You can also change the URL and Depth dynamically via the "Edit URL" button in the web interface.*

3. For macOS, please disable the system AirPlay Receiver which occupies port 5000. Or use "http://127.0.0.1:5000".

### Docker
1. Build the image:
   ```zsh
   docker build -t triespider .
   ```
2. Run the container:
   ```zsh
   docker run -p 5000:5000 triespider
   ```
