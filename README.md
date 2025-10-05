# 🕷️ CrawlStudio

Unified wrapper for web crawling tools, inspired by modular, community-driven design.

## 🎯 Vision

CrawlStudio provides a unified Python API for various web crawling backends including Firecrawl, Crawl4AI, Scrapy, and Browser-Use (AI-driven). It emphasizes modularity, ease of use, and intelligent extraction capabilities.

## 📦 Installation

```bash
pip install crawlstudio
```

From source (recommended for contributors):
```bash
git clone https://github.com/aiapicore/CrawlStudio.git
cd CrawlStudio
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .[dev]
```

Optional extras for AI browser backend:
```bash
pip install .[browser-use]
```

## ⚡ Quick Start
- CLI:
```bash
crawlstudio https://example.com --backend firecrawl --format markdown --print markdown
```
- Python:
```python
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend

async def main():
    cfg = CrawlConfig()
    res = await FirecrawlBackend(cfg).crawl("https://example.com", format="markdown")
    print(res.markdown)

asyncio.run(main())
```

## 🔐 Environment
Create a `.env` in the project root if using external services/backends:
```env
FIRECRAWL_API_KEY=your_firecrawl_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

For Browser-Use backend, you must set at least one of `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.

If you use headless browsers (via browser-use), install Playwright runtime:
```bash
python -m pip install playwright
python -m playwright install
```

## 🚀 CLI Usage
After install, use the CLI to crawl a URL with different backends and formats:
```bash
crawlstudio https://en.wikipedia.org/wiki/Switzerland --backend firecrawl --format markdown --print markdown
crawlstudio https://en.wikipedia.org/wiki/Switzerland --backend crawl4ai --format html --print html
crawlstudio https://en.wikipedia.org/wiki/Switzerland --backend scrapy --format markdown --print markdown
crawlstudio https://en.wikipedia.org/wiki/Switzerland --backend browser-use --format markdown --print markdown
```
- `--backend`: one of `firecrawl`, `crawl4ai`, `scrapy`, `browser-use`
- `--format`: one of `markdown`, `html`, `structured`
- `--print`: choose what to print: `summary` (default), `markdown`, `html`, `structured`

## 📘 Usage Examples (API)
The library exposes a unified interface; below are end-to-end examples for each backend.

### 🧑‍💻 Python Usage
```python
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend

async def main():
    config = CrawlConfig()
    backend = FirecrawlBackend(config)
    result = await backend.crawl("https://en.wikipedia.org/wiki/Switzerland", format="markdown")
    print(result.markdown)

asyncio.run(main())
```

### Firecrawl Example
```python
import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend

async def main():
    config = CrawlConfig()
    backend = FirecrawlBackend(config)
    result = await backend.crawl("https://en.wikipedia.org/wiki/Switzerland", format="markdown")
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
    result = await backend.crawl("https://en.wikipedia.org/wiki/Switzerland", format="markdown")
    print(result.markdown)  # Outputs title, summary, keywords

asyncio.run(main())
```

### Scrapy Example
```python
import asyncio
from crawlstudio import CrawlConfig, ScrapyBackend

async def main():
    config = CrawlConfig()
    backend = ScrapyBackend(config)
    result = await backend.crawl("https://en.wikipedia.org/wiki/Switzerland", format="html")
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
    result = await backend.crawl("https://en.wikipedia.org/wiki/Switzerland", format="markdown")
    print(result.markdown)  # AI-extracted data

asyncio.run(main())
```

## 🧪 Tests & Checks
Run the test suite (pytest) and local checks (flake8, mypy):
```bash
pytest -q
flake8
mypy crawlstudio
```
Notes:
- We target Python 3.10+ for typing (PEP 604 `X | Y` unions).
- Third-party libraries without type stubs are ignored by mypy (`ignore_missing_imports = true`).

## 🛠️ Contributing Quickstart
- Fork and clone the repo, create a virtual env, then install dev deps:
```bash
git clone https://github.com/aiapicore/CrawlStudio.git
cd CrawlStudio
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```
- Optional: install pre-commit hooks
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
- Run the suite before submitting a PR:
```bash
flake8
mypy crawlstudio
pytest -q
```

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