# CrawlStudio Examples

This directory contains example scripts and demonstrations of CrawlStudio functionality.

## Files

### `demo.py` 
Comprehensive demonstration of all CrawlStudio backends with performance comparison.

**Usage:**
```bash
python examples/demo.py
```

**What it shows:**
- All 3 backends working (Firecrawl, Crawl4AI, Scrapy)
- Performance comparison across formats
- Capability analysis
- Recommendations for different use cases

## Running Examples

Make sure you have set up your environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys in .env file
FIRECRAWL_API_KEY=your_key_here

# Run the demo
python examples/demo.py
```

## Expected Output

The demo will show:
- Markdown format comparison (Firecrawl: fastest, Crawl4AI: comprehensive, Scrapy: no markdown)
- HTML format comparison (all backends working)
- Structured format comparison (all backends with different approaches)
- Performance metrics and recommendations

## Use Cases

- **Firecrawl**: Best for production use with API key
- **Crawl4AI**: Best for local development and testing
- **Scrapy**: Best for pure HTML extraction needs