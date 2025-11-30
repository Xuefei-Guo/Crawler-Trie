FROM python:3.10-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY trie_search/ trie_search/

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 5000

# Environment variables
ENV URL="https://example.com"
ENV DEPTH=2

# Run the application
CMD ["uv", "run", "flask", "--app", "trie_search.web", "run", "--host=0.0.0.0"]
