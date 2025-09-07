#!/usr/bin/env python3
"""
Guardian Website Crawling Comparison - All 4 Backends
Tests how each backend handles The Guardian's content extraction
"""

import asyncio
import json
import time
import sys
import os
from typing import Dict, Any

# Fix Windows console Unicode issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from crawlstudio import CrawlConfig, FirecrawlBackend, Crawl4AIBackend, ScrapyBackend, BrowserUseBackend

GUARDIAN_URL = "https://www.theguardian.com"

async def test_backend(backend_name: str, backend, url: str, format: str = "markdown") -> Dict[str, Any]:
    """Test a single backend and return results"""
    print(f"\n🔄 Testing {backend_name} backend...")
    
    start_time = time.time()
    try:
        result = await backend.crawl(url, format=format)
        end_time = time.time()
        
        # Analyze content
        markdown_length = len(result.markdown) if result.markdown else 0
        html_length = len(result.raw_html) if result.raw_html else 0
        has_structured = result.structured_data is not None and len(str(result.structured_data)) > 10
        
        return {
            "backend": backend_name,
            "success": True,
            "duration": round(end_time - start_time, 2),
            "markdown_length": markdown_length,
            "html_length": html_length,
            "has_structured_data": has_structured,
            "metadata": result.metadata,
            "sample_content": result.markdown[:500] + "..." if result.markdown and len(result.markdown) > 500 else result.markdown,
            "error": None
        }
        
    except Exception as e:
        end_time = time.time()
        return {
            "backend": backend_name,
            "success": False,
            "duration": round(end_time - start_time, 2),
            "error": str(e),
            "markdown_length": 0,
            "html_length": 0,
            "has_structured_data": False,
            "metadata": None,
            "sample_content": None
        }

async def test_recursive_links(backend, url: str) -> Dict[str, Any]:
    """Test finding links for recursive crawling"""
    try:
        result = await backend.crawl(url, format="structured")
        
        # Extract links from structured data or markdown
        links = []
        if result.structured_data and isinstance(result.structured_data, dict):
            # Look for links in structured data
            for key, value in result.structured_data.items():
                if 'link' in key.lower() or 'url' in key.lower():
                    if isinstance(value, list):
                        links.extend([link for link in value if isinstance(link, str) and 'theguardian.com' in link])
                    elif isinstance(value, str) and 'theguardian.com' in value:
                        links.append(value)
        
        # Also check markdown for guardian links
        if result.markdown:
            import re
            markdown_links = re.findall(r'\[([^\]]+)\]\((https://www\.theguardian\.com[^\)]+)\)', result.markdown)
            links.extend([link[1] for link in markdown_links])
        
        return {
            "found_links": len(set(links)),  # Remove duplicates
            "sample_links": list(set(links))[:5],  # First 5 unique links
            "success": True
        }
        
    except Exception as e:
        return {
            "found_links": 0,
            "sample_links": [],
            "success": False,
            "error": str(e)
        }

async def main():
    """Run comprehensive Guardian website comparison"""
    print("🏆 CrawlStudio Guardian Website Comparison")
    print("=" * 60)
    print(f"Target URL: {GUARDIAN_URL}")
    print(f"Testing 4 backends: Firecrawl, Crawl4AI, Scrapy, Browser-Use")
    print("=" * 60)
    
    config = CrawlConfig()
    
    # Initialize all backends
    backends = {
        "Firecrawl": FirecrawlBackend(config),
        "Crawl4AI": Crawl4AIBackend(config),
        "Scrapy": ScrapyBackend(config),
    }
    
    # Try to add Browser-Use if available
    try:
        backends["Browser-Use"] = BrowserUseBackend(config)
        print("✅ All 4 backends available")
    except Exception as e:
        print(f"⚠️  Browser-Use backend not available: {e}")
        print("📝 Install with: pip install browser-use langchain-openai")
    
    results = []
    
    # Test each backend
    for backend_name, backend in backends.items():
        result = await test_backend(backend_name, backend, GUARDIAN_URL, "markdown")
        results.append(result)
        
        if result["success"]:
            print(f"✅ {backend_name}: {result['duration']}s, {result['markdown_length']} chars markdown")
        else:
            print(f"❌ {backend_name}: Failed - {result['error']}")
    
    print("\n🔗 Testing Recursive Crawling Capabilities")
    print("-" * 40)
    
    # Test recursive link discovery
    for backend_name, backend in backends.items():
        if any(r["backend"] == backend_name and r["success"] for r in results):
            print(f"\n🔄 Finding links with {backend_name}...")
            recursive_result = await test_recursive_links(backend, GUARDIAN_URL)
            
            if recursive_result["success"]:
                print(f"✅ Found {recursive_result['found_links']} Guardian links")
                if recursive_result['sample_links']:
                    print("📋 Sample links:")
                    for link in recursive_result['sample_links']:
                        print(f"   - {link}")
            else:
                print(f"❌ Failed to find links: {recursive_result.get('error', 'Unknown error')}")
    
    print("\n📊 BACKEND COMPARISON SUMMARY")
    print("=" * 60)
    
    # Create comparison table
    successful_results = [r for r in results if r["success"]]
    
    if successful_results:
        print(f"{'Backend':<12} {'Speed':<8} {'Markdown':<10} {'HTML':<8} {'Structured':<10}")
        print("-" * 60)
        
        for result in successful_results:
            structured = "Yes" if result["has_structured_data"] else "No"
            print(f"{result['backend']:<12} {result['duration']:<8}s {result['markdown_length']:<10} {result['html_length']:<8} {structured:<10}")
        
        # Show content quality comparison
        print("\n📖 CONTENT QUALITY SAMPLES")
        print("-" * 40)
        
        for result in successful_results:
            if result["sample_content"]:
                print(f"\n🔹 {result['backend']} Sample:")
                print(result["sample_content"][:300] + "..." if len(result["sample_content"]) > 300 else result["sample_content"])
        
        # Performance ranking
        print(f"\n🏃 SPEED RANKING (fastest to slowest):")
        sorted_results = sorted(successful_results, key=lambda x: x["duration"])
        for i, result in enumerate(sorted_results, 1):
            print(f"  {i}. {result['backend']}: {result['duration']}s")
    
    else:
        print("❌ No backends succeeded. Check your API keys and network connection.")
    
    print("\n🎯 RECOMMENDATIONS FOR GUARDIAN.COM:")
    print("-" * 40)
    print("• Firecrawl: Best for production Guardian scraping (fast, reliable)")
    print("• Crawl4AI: Good for free development and testing")  
    print("• Scrapy: Best for simple HTML extraction (fastest)")
    print("• Browser-Use: Best for AI-powered content understanding")
    
    print("\n🔄 RECURSIVE CRAWLING NOTES:")
    print("-" * 40)
    print("• All backends can extract links from Guardian pages")
    print("• Implement batch processing for multiple URLs")
    print("• Consider rate limiting for Guardian's servers")
    print("• Use structured extraction to find article links specifically")

if __name__ == "__main__":
    asyncio.run(main())