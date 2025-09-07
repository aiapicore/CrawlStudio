#!/usr/bin/env python3
"""
CrawlStudio Recursive Crawling Demo
Demonstrates multi-page crawling capabilities using The Guardian
"""

import asyncio
import json
import time
import sys
import os
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse

# Fix Windows console Unicode issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from crawlstudio import CrawlConfig, FirecrawlBackend, Crawl4AIBackend, ScrapyBackend

class RecursiveCrawler:
    """Demonstrates recursive crawling with different backends"""
    
    def __init__(self, backend, max_pages: int = 3, delay: float = 1.0):
        self.backend = backend
        self.max_pages = max_pages
        self.delay = delay  # Rate limiting
        self.crawled_urls = set()
        self.results = []
        
    async def extract_guardian_links(self, content: str, base_url: str) -> List[str]:
        """Extract Guardian article links from content"""
        import re
        
        # Pattern to find Guardian article URLs
        patterns = [
            r'https://www\.theguardian\.com/[a-zA-Z-]+/\d{4}/[a-zA-Z0-9/-]+',
            r'\[([^\]]+)\]\((https://www\.theguardian\.com/[^\)]+)\)',
        ]
        
        links = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    links.add(match[1])  # URL from markdown link
                else:
                    links.add(match)  # Direct URL
        
        # Filter to only article links (not categories, etc.)
        article_links = []
        for link in links:
            parsed = urlparse(link)
            path_parts = parsed.path.strip('/').split('/')
            # Article URLs typically have: /section/year/month/day/article-title
            if len(path_parts) >= 5 and path_parts[1].isdigit() and len(path_parts[1]) == 4:
                article_links.append(link)
        
        return list(set(article_links))[:5]  # Return max 5 unique links
    
    async def crawl_recursive(self, start_url: str) -> Dict[str, Any]:
        """Perform recursive crawling starting from URL"""
        print(f"\n🕷️  Starting recursive crawl with {self.backend.__class__.__name__}")
        print(f"📍 Start URL: {start_url}")
        print(f"📏 Max pages: {self.max_pages}")
        print("-" * 60)
        
        queue = [start_url]
        crawl_results = []
        
        while queue and len(self.crawled_urls) < self.max_pages:
            current_url = queue.pop(0)
            
            if current_url in self.crawled_urls:
                continue
                
            print(f"\n🔄 Crawling page {len(self.crawled_urls) + 1}: {current_url[:80]}...")
            
            try:
                start_time = time.time()
                result = await self.backend.crawl(current_url, format="markdown")
                duration = time.time() - start_time
                
                self.crawled_urls.add(current_url)
                
                # Extract content info
                content_length = len(result.markdown) if result.markdown else 0
                title = "Unknown"
                
                # Try to extract title from markdown
                if result.markdown:
                    lines = result.markdown.split('\n')
                    for line in lines:
                        if line.startswith('# '):
                            title = line[2:].strip()[:100]
                            break
                
                page_result = {
                    "url": current_url,
                    "title": title,
                    "content_length": content_length,
                    "duration": round(duration, 2),
                    "success": True
                }
                
                crawl_results.append(page_result)
                
                print(f"✅ Success: '{title}' ({content_length} chars, {duration:.2f}s)")
                
                # Find more links to crawl
                if len(self.crawled_urls) < self.max_pages:
                    new_links = await self.extract_guardian_links(result.markdown or "", current_url)
                    added_links = 0
                    for link in new_links:
                        if link not in self.crawled_urls and link not in queue:
                            queue.append(link)
                            added_links += 1
                    
                    if added_links > 0:
                        print(f"🔗 Found {added_links} new article links")
                
                # Rate limiting
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
                    
            except Exception as e:
                print(f"❌ Failed: {str(e)[:100]}")
                page_result = {
                    "url": current_url,
                    "title": "Failed",
                    "content_length": 0,
                    "duration": 0,
                    "success": False,
                    "error": str(e)
                }
                crawl_results.append(page_result)
        
        return {
            "backend": self.backend.__class__.__name__,
            "start_url": start_url,
            "pages_crawled": len(self.crawled_urls),
            "total_content": sum(r["content_length"] for r in crawl_results if r["success"]),
            "total_time": sum(r["duration"] for r in crawl_results),
            "success_rate": len([r for r in crawl_results if r["success"]]) / len(crawl_results) * 100,
            "results": crawl_results
        }

async def compare_recursive_crawling():
    """Compare recursive crawling across backends"""
    print("🕸️  CrawlStudio Recursive Crawling Comparison")
    print("=" * 70)
    print("Testing multi-page crawling of Guardian articles")
    print("=" * 70)
    
    config = CrawlConfig()
    guardian_home = "https://www.theguardian.com"
    max_pages = 3  # Keep it small for demo
    
    # Initialize backends
    backends = {
        "Firecrawl": FirecrawlBackend(config),
        "Crawl4AI": Crawl4AIBackend(config),
        "Scrapy": ScrapyBackend(config)  # Scrapy won't extract good links but we'll show the difference
    }
    
    all_results = []
    
    for backend_name, backend in backends.items():
        crawler = RecursiveCrawler(backend, max_pages=max_pages, delay=0.5)  # 0.5s delay between requests
        result = await crawler.crawl_recursive(guardian_home)
        all_results.append(result)
    
    print("\n📊 RECURSIVE CRAWLING COMPARISON")
    print("=" * 70)
    
    # Summary table
    print(f"{'Backend':<12} {'Pages':<6} {'Success%':<8} {'Total Chars':<12} {'Total Time':<10}")
    print("-" * 70)
    
    for result in all_results:
        print(f"{result['backend']:<12} {result['pages_crawled']:<6} {result['success_rate']:<7.1f}% {result['total_content']:<12} {result['total_time']:<9.1f}s")
    
    # Detailed results
    print("\n📖 DETAILED CRAWLING RESULTS")
    print("-" * 70)
    
    for result in all_results:
        print(f"\n🔹 {result['backend']} Results:")
        for i, page in enumerate(result['results'], 1):
            status = "✅" if page['success'] else "❌"
            print(f"   {i}. {status} {page['title'][:60]} ({page['content_length']} chars)")
    
    # Analysis
    print("\n🧠 RECURSIVE CRAWLING ANALYSIS")
    print("-" * 70)
    
    best_coverage = max(all_results, key=lambda x: x['pages_crawled'])
    fastest = min([r for r in all_results if r['pages_crawled'] > 0], key=lambda x: x['total_time'] / max(x['pages_crawled'], 1))
    most_content = max(all_results, key=lambda x: x['total_content'])
    
    print(f"🎯 Best Coverage: {best_coverage['backend']} ({best_coverage['pages_crawled']} pages)")
    print(f"⚡ Fastest per Page: {fastest['backend']} ({fastest['total_time']/max(fastest['pages_crawled'], 1):.2f}s average)")
    print(f"📚 Most Content: {most_content['backend']} ({most_content['total_content']} total chars)")
    
    print("\n💡 RECURSIVE CRAWLING INSIGHTS:")
    print("-" * 40)
    print("• Firecrawl & Crawl4AI extract clean markdown with links")
    print("• Scrapy gets raw HTML but struggles with link extraction") 
    print("• Content-aware backends find more article links")
    print("• Rate limiting is essential for respectful crawling")
    print("• Guardian has sophisticated link structures")
    
    print("\n🛠️  IMPLEMENTATION RECOMMENDATIONS:")
    print("-" * 40)
    print("• Use Firecrawl for production recursive crawling")
    print("• Implement exponential backoff for rate limiting")
    print("• Filter links by content type (articles vs categories)")
    print("• Store crawled URLs to avoid duplicates")
    print("• Consider robots.txt compliance")
    print("• Use structured extraction for better link discovery")
    
    return all_results

async def main():
    """Main demo function"""
    results = await compare_recursive_crawling()
    
    print("\n🚀 CrawlStudio Recursive Crawling Demo Complete!")
    print(f"Successfully demonstrated multi-page crawling with {len(results)} backends")

if __name__ == "__main__":
    asyncio.run(main())