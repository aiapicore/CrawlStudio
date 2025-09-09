"""
Comprehensive test for all Firecrawl features
"""
import asyncio
import os
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, FirecrawlBackend

load_dotenv()


@pytest.mark.asyncio
async def test_all_formats():
    print("="*60)
    print("COMPREHENSIVE FIRECRAWL TEST")
    print("="*60)

    config = CrawlConfig()
    if not config.firecrawl_api_key:
        print("ERROR: FIRECRAWL_API_KEY not found in .env file")
        return

    backend = FirecrawlBackend(config)
    test_url = "https://httpbin.org/html"

    # Test 1: Markdown format
    print("\n1. Testing MARKDOWN format...")
    try:
        result = await backend.crawl(test_url, format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown)} chars")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Cache hit: {result.cache_hit}")
        print(f"   Metadata keys: {list(result.metadata.keys())}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 2: HTML format
    print("\n2. Testing HTML format...")
    try:
        result = await backend.crawl(test_url, format="html")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown) if result.markdown else 0} chars")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Cache hit: {result.cache_hit}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 3: Structured format
    print("\n3. Testing STRUCTURED format...")
    try:
        result = await backend.crawl(test_url, format="structured")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Structured data: {result.structured_data}")
        print(f"   Cache hit: {result.cache_hit}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 4: Error handling
    print("\n4. Testing ERROR handling...")
    try:
        result = await backend.crawl("invalid-url-format", format="markdown")
        print(f"   UNEXPECTED SUCCESS: {result}")
    except Exception as e:
        print(f"   SUCCESS: Error properly caught - {str(e)[:100]}...")

    # Test 5: Different website
    print("\n5. Testing different website...")
    try:
        result = await backend.crawl("https://example.com", format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Markdown: {len(result.markdown)} chars")
        print(f"   Title in metadata: {'title' in result.metadata}")
    except Exception as e:
        print(f"   FAILED: {e}")

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_all_formats())
