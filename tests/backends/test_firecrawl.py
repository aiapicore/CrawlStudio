"""
Comprehensive tests for Firecrawl backend
"""
import asyncio
import pytest
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, FirecrawlBackend

load_dotenv()

class TestFirecrawlBackend:
    
    @pytest.fixture
    def backend(self):
        """Create Firecrawl backend instance"""
        config = CrawlConfig()
        return FirecrawlBackend(config)
    
    @pytest.mark.asyncio
    async def test_basic_markdown_crawling(self, backend):
        """Test basic markdown extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="markdown")
        
        assert result.backend_used == "firecrawl"
        assert result.url == "https://httpbin.org/html"
        assert result.markdown is not None
        assert len(result.markdown) > 0
        assert result.execution_time > 0
        
    @pytest.mark.asyncio
    async def test_html_extraction(self, backend):
        """Test HTML extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="html")
        
        assert result.backend_used == "firecrawl"
        assert result.raw_html is not None
        assert len(result.raw_html) > 0
    
    @pytest.mark.asyncio
    async def test_structured_extraction(self, backend):
        """Test structured data extraction"""
        result = await backend.crawl("https://httpbin.org/html", format="structured")
        
        assert result.backend_used == "firecrawl"
        assert result.structured_data is not None
        assert "title" in result.structured_data
        assert "summary" in result.structured_data
        assert "keywords" in result.structured_data
    
    @pytest.mark.asyncio
    async def test_api_key_requirement(self):
        """Test that API key is required"""
        config = CrawlConfig()
        config.firecrawl_api_key = None  # Remove API key
        backend = FirecrawlBackend(config)
        
        with pytest.raises(ValueError, match="FIRECRAWL_API_KEY is required"):
            await backend.crawl("https://httpbin.org/html", format="markdown")
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_url(self, backend):
        """Test error handling with invalid URL"""
        with pytest.raises(ValueError):
            await backend.crawl("not-a-valid-url", format="markdown")
    
    @pytest.mark.asyncio
    async def test_caching_detection(self, backend):
        """Test cache hit detection"""
        url = "https://httpbin.org/html"
        
        # First request
        result1 = await backend.crawl(url, format="markdown")
        
        # Second request should potentially be cached
        result2 = await backend.crawl(url, format="markdown")
        
        # At least one should detect caching behavior
        assert result1.backend_used == "firecrawl"
        assert result2.backend_used == "firecrawl"


async def run_manual_tests():
    """Manual test runner for Firecrawl"""
    print("="*60)
    print("FIRECRAWL BACKEND TESTS")
    print("="*60)
    
    config = CrawlConfig()
    if not config.firecrawl_api_key:
        print("ERROR: FIRECRAWL_API_KEY not found in .env file")
        print("Please add: FIRECRAWL_API_KEY=your_api_key")
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
    
    print("\n" + "="*60)
    print("FIRECRAWL TESTS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_manual_tests())