# CrawlStudio Documentation

Welcome to CrawlStudio - the unified Python library for web crawling tools!

## Overview

CrawlStudio provides a unified API for various web crawling backends including:

- **Firecrawl** - Production-ready API service
- **Crawl4AI** - Free, comprehensive local crawler  
- **Scrapy** - Fast HTML extraction framework
- **Browser-Use** - AI-driven browser automation

## Quick Start

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

## Key Features

- ✅ **4 Working Backends** with unified interface
- ✅ **Multiple Output Formats** (markdown, HTML, structured data)  
- ✅ **Async/Await Support** for high performance
- ✅ **Cross-Platform** compatibility (Windows, Linux, macOS)
- ✅ **Professional Testing** with comprehensive test suite

## Navigation

- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api/models.md) - Complete API documentation
- [Examples](examples.md) - Code examples and tutorials
- [Contributing](CONTRIBUTING.md) - How to contribute to the project