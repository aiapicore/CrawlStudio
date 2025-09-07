# Browser-Use Backend Setup

CrawlStudio now supports **Browser-Use** - an AI-driven web automation backend that can intelligently interact with web pages!

## 🤖 What is Browser-Use Backend?

Unlike traditional scrapers, the Browser-Use backend uses **AI agents** to:
- **Understand web page context** 
- **Perform intelligent interactions**
- **Extract data based on intent** rather than just structure
- **Handle complex dynamic websites**
- **Navigate and interact** like a human would

## 🛠️ Installation

### 1. Install Browser-Use Package

```bash
pip install browser-use
```

### 2. Install Browser Dependencies

```bash
# Install Chromium for browser automation
uvx playwright install chromium --with-deps
```

### 3. Set up AI API Keys

Add to your `.env` file:

```bash
# For OpenAI (recommended)
OPENAI_API_KEY=sk-your-openai-key-here

# OR for Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-key-here
```

### 4. Install LangChain Dependencies

```bash
# For OpenAI
pip install langchain-openai

# OR for Anthropic  
pip install langchain-anthropic
```

## 🚀 Usage Examples

### Basic Usage

```python
import asyncio
from crawlstudio import CrawlConfig, BrowserUseBackend

async def main():
    config = CrawlConfig()
    backend = BrowserUseBackend(config)
    
    # AI will intelligently extract content
    result = await backend.crawl(
        "https://example.com", 
        format="structured"
    )
    
    print(f"AI extracted: {result.structured_data}")

asyncio.run(main())
```

### Markdown Extraction

```python
# AI understands content structure and converts to markdown
result = await backend.crawl(
    "https://news-site.com/article", 
    format="markdown"
)
print(result.markdown)  # Clean, structured markdown
```

### Structured Data Extraction

```python
# AI extracts key information intelligently
result = await backend.crawl(
    "https://product-page.com", 
    format="structured"
)

data = result.structured_data
print(f"Title: {data['title']}")
print(f"Summary: {data['summary']}")
print(f"Keywords: {data['keywords']}")
```

## 🎯 When to Use Browser-Use Backend

### ✅ **Perfect For:**
- **Complex dynamic websites** with JavaScript
- **Content that requires context understanding**
- **Sites that need intelligent interaction**
- **Data extraction that benefits from AI**
- **Pages that traditional scrapers struggle with**

### ⚠️ **Consider Alternatives For:**
- **Simple static HTML** (use Scrapy - faster)
- **High-volume batch processing** (use Firecrawl - more efficient)
- **Cost-sensitive applications** (AI API calls cost money)
- **Real-time scraping** (AI processing takes longer)

## 💰 Cost Considerations

Browser-Use backend uses AI APIs:
- **OpenAI GPT-4o-mini**: ~$0.15 per 1M input tokens
- **Anthropic Claude Haiku**: ~$0.25 per 1M tokens
- **Typical webpage**: ~1,000-5,000 tokens
- **Cost per page**: ~$0.0001-0.0005 (very affordable!)

## 🔧 Configuration Options

```python
# The backend automatically:
# - Chooses cost-effective AI models (GPT-4o-mini, Claude Haiku)
# - Limits actions to prevent runaway agents
# - Uses separate browser instances for isolation
# - Provides intelligent error handling
```

## 🧪 Testing

```bash
# Test if browser-use is working
python simple_browser_use_test.py

# Run all backend tests including browser-use
python tests/run_all_tests.py
```

## 🆚 Backend Comparison

| Backend | Speed | Cost | Intelligence | Best For |
|---------|-------|------|--------------|----------|
| **Firecrawl** | Fast | API costs | Medium | Production |
| **Crawl4AI** | Medium | Free | Medium | Development |
| **Scrapy** | Fast | Free | Low | Simple HTML |
| **Browser-Use** | Slower | AI costs | **High** | **Complex sites** |

## 🎉 Advanced Example

```python
async def intelligent_scraping():
    backend = BrowserUseBackend(config)
    
    # AI can handle complex extraction tasks
    result = await backend.crawl(
        "https://e-commerce-site.com/product/123",
        format="structured"
    )
    
    # AI understands product pages and extracts:
    # - Product name, price, description
    # - Reviews and ratings
    # - Technical specifications
    # - Related products
    
    return result.structured_data
```

The Browser-Use backend brings **AI intelligence** to web scraping, making it possible to extract data from complex sites that would be difficult with traditional approaches!

## 🚨 Important Notes

- **Requires AI API key** (OpenAI or Anthropic)
- **Slower than traditional backends** (AI processing time)
- **More expensive** (AI API costs)
- **More powerful** for complex extraction tasks
- **Better at understanding context** and content meaning