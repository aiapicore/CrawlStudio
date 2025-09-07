# Getting Started

## Installation

### Basic Installation

```bash
pip install crawlstudio
```

### With Optional Dependencies

```bash
# For Browser-Use backend (AI-driven)
pip install crawlstudio[browser-use]

# For development
pip install crawlstudio[dev]
```

## Configuration

Create a `.env` file with your API keys:

```bash
FIRECRAWL_API_KEY=your-firecrawl-key
OPENAI_API_KEY=your-openai-key  # For Browser-Use backend
ANTHROPIC_API_KEY=your-anthropic-key  # Alternative for Browser-Use
```

## Basic Usage

### Simple Crawling

```python
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend

async def main():
    config = CrawlConfig()
    backend = FirecrawlBackend(config)
    result = await backend.crawl("https://example.com", format="markdown")
    print(result.markdown)

asyncio.run(main())
```

### Different Formats

```python
# Get clean markdown
result = await backend.crawl(url, format="markdown")
print(result.markdown)

# Get raw HTML
result = await backend.crawl(url, format="html") 
print(result.raw_html)

# Get structured data
result = await backend.crawl(url, format="structured")
print(result.structured_data)
```

### Different Backends

```python
from crawlstudio import FirecrawlBackend, Crawl4AIBackend, ScrapyBackend

# Production-ready with API
backend = FirecrawlBackend(config)

# Free local processing  
backend = Crawl4AIBackend(config)

# Fast HTML extraction
backend = ScrapyBackend(config)
```

## Next Steps

- Check out [Examples](examples.md) for more use cases
- Read [API Reference](api/models.md) for complete documentation
- See [Contributing](CONTRIBUTING.md) to help improve CrawlStudio