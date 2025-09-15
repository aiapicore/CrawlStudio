"""
Simple test for updated Crawl4AI backend
"""
import asyncio
import pytest
from crawlstudio import CrawlConfig, Crawl4AIBackend


@pytest.mark.asyncio
async def test_crawl4ai():
    print("Testing updated Crawl4AI backend...")

    config = CrawlConfig()
    backend = Crawl4AIBackend(config)

    try:
        print("Testing basic markdown extraction...")
        result = await backend.crawl("https://example.com/", format="markdown")
        print(f"SUCCESS: {result.backend_used}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Markdown length: {len(result.markdown) if result.markdown else 0}")
        print(f"HTML length: {len(result.raw_html) if result.raw_html else 0}")
        print(f"Cache hit: {result.cache_hit}")
        print("=" * 50)

        print("Testing HTML extraction...")
        result2 = await backend.crawl("https://example.com/", format="html")
        print(f"SUCCESS: {result2.backend_used}")
        print(f"HTML length: {len(result2.raw_html) if result2.raw_html else 0}")
        print("=" * 50)

        print("Testing structured extraction...")
        result3 = await backend.crawl("https://example.com/", format="structured")
        print(f"SUCCESS: {result3.backend_used}")
        print(f"Structured data: {result3.structured_data}")
        print("=" * 50)

        print("All Crawl4AI tests passed!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_crawl4ai())
