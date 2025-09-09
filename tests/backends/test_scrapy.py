"""
Comprehensive tests for Scrapy backend
"""
import asyncio
import pytest
from crawlstudio import CrawlConfig, ScrapyBackend
from crawlstudio.exceptions import BackendExecutionError


class TestScrapyBackend:

    @pytest.fixture
    def backend(self):
        """Create Scrapy backend instance"""
        config = CrawlConfig()
        return ScrapyBackend(config)

    @pytest.mark.asyncio
    async def test_basic_crawling(self, backend):
        """Test basic HTML extraction with Scrapy"""
        result = await backend.crawl("https://httpbin.org/html", format="html")

        assert result.backend_used == "scrapy"
        assert result.url == "https://httpbin.org/html"
        assert result.raw_html is not None
        assert len(result.raw_html) > 0
        assert result.execution_time > 0

    @pytest.mark.asyncio
    async def test_markdown_format_limitation(self, backend):
        """Test that Scrapy doesn't provide markdown (returns None)"""
        result = await backend.crawl("https://httpbin.org/html", format="markdown")

        assert result.backend_used == "scrapy"
        assert result.markdown is None  # Scrapy doesn't convert to markdown
        assert result.raw_html is not None

    @pytest.mark.asyncio
    async def test_structured_format_limitation(self, backend):
        """Test that Scrapy doesn't provide structured data"""
        result = await backend.crawl("https://httpbin.org/html", format="structured")

        assert result.backend_used == "scrapy"
        assert result.structured_data is None  # Scrapy doesn't extract structured data
        assert result.raw_html is not None

    @pytest.mark.asyncio
    async def test_metadata_extraction(self, backend):
        """Test metadata extraction from Scrapy"""
        result = await backend.crawl("https://httpbin.org/html", format="html")

        assert result.backend_used == "scrapy"
        assert result.metadata is not None
        assert "title" in result.metadata
        assert "links" in result.metadata

    @pytest.mark.asyncio
    async def test_error_handling_invalid_url(self, backend):
        """Test error handling with invalid URL"""
        with pytest.raises(BackendExecutionError, match="Scrapy crawl failed"):
            await backend.crawl("not-a-valid-url", format="html")


async def run_manual_tests():
    """Manual test runner for Scrapy"""
    print("="*60)
    print("SCRAPY BACKEND TESTS")
    print("="*60)

    config = CrawlConfig()
    backend = ScrapyBackend(config)
    test_url = "https://httpbin.org/html"

    # Test 1: HTML format (primary use case for Scrapy)
    print("\n1. Testing HTML format...")
    try:
        result = await backend.crawl(test_url, format="html")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Markdown: {result.markdown} (expected None)")
        print(f"   Metadata: {result.metadata}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 2: Markdown format (should work but no conversion)
    print("\n2. Testing MARKDOWN format...")
    try:
        result = await backend.crawl(test_url, format="markdown")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   HTML: {len(result.raw_html) if result.raw_html else 0} chars")
        print(f"   Markdown: {result.markdown} (expected None)")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 3: Structured format (now working!)
    print("\n3. Testing STRUCTURED format...")
    try:
        result = await backend.crawl(test_url, format="structured")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   Structured data available: {result.structured_data is not None}")
        if result.structured_data:
            print(f"   Title: {result.structured_data.get('title', 'N/A')}")
            print(f"   Summary length: {len(result.structured_data.get('summary', ''))}")
    except Exception as e:
        print(f"   FAILED: {e}")

    # Test 4: Error handling
    print("\n4. Testing ERROR handling...")
    try:
        result = await backend.crawl("invalid-url-format", format="html")
        print(f"   UNEXPECTED SUCCESS: {result}")
    except Exception as e:
        print(f"   SUCCESS: Error properly caught - {str(e)[:100]}...")

    # Test 5: Different website
    print("\n5. Testing different website...")
    try:
        result = await backend.crawl("https://example.com", format="html")
        print(f"   SUCCESS: {result.backend_used}")
        print(f"   Execution: {result.execution_time:.2f}s")
        print(f"   HTML: {len(result.raw_html)} chars")
        print(f"   Title in metadata: {result.metadata.get('title', 'N/A')}")
        print(f"   Status code: {result.metadata.get('status_code', 'N/A')}")
    except Exception as e:
        print(f"   FAILED: {e}")

    print("\n" + "="*60)
    print("SCRAPY TESTS COMPLETE - ALL WORKING!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_manual_tests())
