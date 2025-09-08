# 🕷️ CrawlStudio

Unified wrapper for web crawling tools, inspired by modular, community-driven design.

## 🎯 Vision

CrawlStudio provides a unified Python API for various web crawling backends including Firecrawl, Crawl4AI, Scrapy, and Browser-Use (AI-driven). It emphasizes modularity, ease of use, and intelligent extraction capabilities.

## 📦 Installation

```bash
pip install crawlstudio
```

## 🚀 Usage Examples

### Firecrawl Example

```python
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend

async def main():
    config = CrawlConfig()
    backend = FirecrawlBackend(config)
    result = await backend.crawl("https://www.bloomberg.com/", format="markdown")
    print(result.markdown)

asyncio.run(main())
```

### Crawl4AI Example

```python
import asyncio
from crawlstudio import CrawlConfig, Crawl4AIBackend

async def main():
    config = CrawlConfig()
    backend = Crawl4AIBackend(config)
    result = await backend.crawl("https://finance.yahoo.com/", format="structured")
    print(result.structured_data)  # Outputs title, summary, keywords

asyncio.run(main())
```

### Scrapy Example

```python
import asyncio
from crawlstudio import CrawlConfig, ScrapyBackend

async def main():
    config = CrawlConfig()
    backend = ScrapyBackend(config)
    result = await backend.crawl("https://www.bloomberg.com/", format="html")
    print(result.raw_html)

asyncio.run(main())
```

### Browser-Use (AI-Driven) Example

```python
import asyncio
from crawlstudio import CrawlConfig, BrowserUseBackend

async def main():
    config = CrawlConfig()
    backend = BrowserUseBackend(config)
    result = await backend.crawl("https://example.com", format="structured")
    print(result.structured_data)  # AI-extracted data

asyncio.run(main())
```

> **Note**: Browser-Use backend requires `pip install browser-use` and an AI API key (OpenAI or Anthropic). See [BROWSER_USE_SETUP.md](BROWSER_USE_SETUP.md) for details.

## ⚡ Backend Comparison

| Backend | Speed | Cost | AI Intelligence | Best For |
|---------|-------|------|----------------|----------|
| **Firecrawl** | Fast | API costs | Medium | Production scraping |
| **Crawl4AI** | Medium | Free | Medium | Development & testing |
| **Scrapy** | Fastest | Free | Low | Simple HTML extraction |
| **Browser-Use** | Slower | AI costs | High | Complex dynamic sites |

## 🔮 Future Enhancements

### Recursive Crawling (Planned)
```python
# Future API - configurable depth and page limits
config = CrawlConfig(
    max_depth=3,                    # Crawl up to 3 levels deep
    max_pages_per_level=5,          # Max 5 pages per depth level
    recursive_delay=1.0,            # 1 second delay between requests
    follow_external_links=False     # Stay within same domain
)

# Recursive crawling with depth control
result = await backend.crawl_recursive("https://example.com", format="markdown")
print(f"Crawled {len(result.pages)} pages across {result.max_depth_reached} levels")
```

### Additional Crawler Backends (Roadmap)

#### High Priority
- **[Playwright](https://github.com/microsoft/playwright-python)** - Fast browser automation, excellent for SPAs
- **[Selenium](https://github.com/SeleniumHQ/selenium)** - Industry standard, huge ecosystem
- **[BeautifulSoup + Requests](https://github.com/psf/requests)** - Lightweight, simple parsing

#### Specialized Crawlers  
- **[Apify SDK](https://github.com/apify/apify-sdk-python)** - Cloud scraping platform
- **[Colly](https://github.com/gocolly/colly)** (via Python bindings) - High-performance Go crawler
- **[Puppeteer](https://github.com/puppeteer/puppeteer)** (via pyppeteer) - Headless Chrome control

#### AI-Enhanced Crawlers
- **[ScrapeGraphAI](https://github.com/VinciGit00/ScrapeGraphAI)** - LLM-powered scraping
- **[AutoScraper](https://github.com/alirezamika/autoscraper)** - Machine learning-based pattern detection
- **[WebGPT](https://github.com/sukhadagholba/webgpt)** - GPT-powered web interaction

#### Enterprise/Commercial
- **[ScrapingBee](https://www.scrapingbee.com/)** - Anti-bot bypass service
- **[Bright Data](https://brightdata.com/)** - Proxy + scraping platform  
- **[Zyte](https://www.zyte.com/)** - Enterprise web data platform

### Advanced Features (Future Versions)
- Multi-page crawling with link discovery
- Batch processing for multiple URLs
- CLI tool (`crawlstudio crawl <url>`)
- Content deduplication and similarity detection
- Rate limiting and respectful crawling policies
- Caching system with Redis/disk storage
- Webhook integrations for real-time notifications
- GraphQL API for programmatic access
- Docker containerization for easy deployment

### Development Roadmap
1. **Core Features** (Current): 4 working backends
2. **Recursive Crawling**: Depth-based multi-page crawling  
3. **CLI Tool**: `pip install crawlstudio` → command line usage
4. **Additional Backends**: Playwright, Selenium, BeautifulSoup
5. **Enterprise Features**: Batch processing, advanced caching
6. **AI Integration**: More AI-powered extraction capabilities
7. **Cloud Platform**: SaaS offering with web interface