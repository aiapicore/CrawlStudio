"""
Simple test for Firecrawl backend
"""
import asyncio
import os
from dotenv import load_dotenv
from crawlstudio import CrawlConfig, FirecrawlBackend

load_dotenv()

async def test_firecrawl():
    print("Testing Firecrawl...")
    
    config = CrawlConfig()
    if not config.firecrawl_api_key:
        print("Error: FIRECRAWL_API_KEY not found in .env file")
        print("Please add your Firecrawl API key to the .env file:")
        print("FIRECRAWL_API_KEY=your_api_key_here")
        return
    
    backend = FirecrawlBackend(config)
    
    try:
        print("Testing basic scrape...")
        result = await backend.crawl("https://httpbin.org/html", format="markdown")
        print(f"SUCCESS: {result.backend_used}")
        print(f"Execution time: {result.execution_time:.2f}s")
        print(f"Markdown length: {len(result.markdown) if result.markdown else 0}")
        print(f"HTML length: {len(result.raw_html) if result.raw_html else 0}")
        print("=" * 50)
        
        print("Testing structured extraction...")
        result2 = await backend.crawl("https://httpbin.org/html", format="structured")
        print(f"Structured data: {result2.structured_data}")
        print("=" * 50)
        
        print("All tests passed!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have a valid Firecrawl API key")

if __name__ == "__main__":
    asyncio.run(test_firecrawl())