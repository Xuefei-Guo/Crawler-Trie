# TrieSpider

A high-performance, asynchronous web crawler and search engine built with Python. It indexes websites using a Trie data structure to provide fast wildcard search and real-time autocomplete capabilities.

## 🚀 Features

- **High Performance Crawler**: Built with `asyncio` and `httpx` for concurrent, non-blocking page fetching.
- **Efficient Search**: Custom Trie implementation supporting wildcard queries (`*`) and prefix-based autocomplete.
- **Real-time Autocomplete**: Interactive frontend with instant search suggestions.
- **Dynamic Configuration**: Manage start URL and crawl depth directly from the web interface without restarting.
- **Containerized**: Docker support for consistent deployment.
- **CI/CD**: Automated testing pipeline using GitHub Actions.

## 🛠️ Technologies

- **Python 3**
- **Flask** (Web Framework)
- **Asyncio & HTTPX** (Concurrency)
- **Docker** (Containerization)
- **Pytest** (Testing)

## 🏃‍♂️ How to Run

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run flask --app trie_search.web run
   ```
   The server will start at `http://127.0.0.1:5000`.
   
   *Default Configuration*: URL=`https://example.com`, Depth=2.

   **Configuration**:
   You can configure the target URL and crawl depth using environment variables OR via the **Edit URL** button in the web UI.
   
   Using environment variables:
   ```bash
   # macOS/Linux
   URL="https://xxxxxxxx" DEPTH=x uv run flask --app trie_search.web run

   # Windows (PowerShell)
   $env:URL="https://xxxxxxxx"; $env:DEPTH=x; uv run flask --app trie_search.web run
   ```

### 🐳 Docker

1. **Build the image**:
   ```bash
   docker build -t triespider .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 triespider
   ```

## 🧪 Running Tests

Run the unit tests to verify the logic:

```bash
uv run python -m pytest
```