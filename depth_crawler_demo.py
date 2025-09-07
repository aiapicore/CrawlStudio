#!/usr/bin/env python3
"""
CrawlStudio True Depth-Based Recursive Crawler
Demonstrates depth-limited crawling (vs page-count limited)
"""

import asyncio
import json
import time
import sys
import os
from typing import List, Dict, Any, Tuple
from urllib.parse import urljoin, urlparse

# Fix Windows console Unicode issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from crawlstudio import CrawlConfig, FirecrawlBackend

class DepthLimitedCrawler:
    """True depth-based recursive crawler"""
    
    def __init__(self, backend, max_depth: int = 3, max_pages_per_level: int = 2):
        self.backend = backend
        self.max_depth = max_depth
        self.max_pages_per_level = max_pages_per_level
        self.crawled_urls = set()
        self.depth_results = {}  # {depth: [results]}
        
    async def extract_guardian_links(self, content: str) -> List[str]:
        """Extract Guardian article links"""
        import re
        
        patterns = [
            r'https://www\.theguardian\.com/[a-zA-Z-]+/\d{4}/[a-zA-Z0-9/-]+',
        ]
        
        links = set()
        for pattern in patterns:
            links.update(re.findall(pattern, content))
        
        # Filter to article links only
        article_links = []
        for link in links:
            parsed = urlparse(link)
            path_parts = parsed.path.strip('/').split('/')
            # Article pattern: /section/year/month/day/title
            if len(path_parts) >= 5 and path_parts[1].isdigit() and len(path_parts[1]) == 4:
                article_links.append(link)
        
        return list(set(article_links))
    
    async def crawl_depth_limited(self, start_url: str) -> Dict[str, Any]:
        """Crawl with true depth limiting"""
        print(f"\n🎯 Depth-Limited Crawling")
        print(f"📍 Start: {start_url}")
        print(f"📊 Max Depth: {self.max_depth}")
        print(f"📄 Max Pages/Level: {self.max_pages_per_level}")
        print("=" * 60)
        
        # Initialize with depth 0
        current_level = [(start_url, 0)]  # (url, depth)
        all_results = []
        
        while current_level:
            next_level = []
            depth = current_level[0][1]  # Current depth
            
            if depth > self.max_depth:
                break
                
            print(f"\n📊 CRAWLING DEPTH {depth}")
            print("-" * 30)
            
            level_results = []
            pages_at_level = 0
            
            for url, url_depth in current_level:
                if url in self.crawled_urls:
                    continue
                    
                if pages_at_level >= self.max_pages_per_level:
                    break
                
                print(f"🔄 Depth {depth}: {url[:80]}...")
                
                try:
                    start_time = time.time()
                    result = await self.backend.crawl(url, format="markdown")
                    duration = time.time() - start_time
                    
                    self.crawled_urls.add(url)
                    pages_at_level += 1
                    
                    # Extract title
                    title = "Unknown"
                    if result.markdown:
                        lines = result.markdown.split('\n')
                        for line in lines:
                            if line.startswith('# '):
                                title = line[2:].strip()[:80]
                                break
                    
                    content_length = len(result.markdown) if result.markdown else 0
                    
                    page_result = {
                        "url": url,
                        "depth": depth,
                        "title": title,
                        "content_length": content_length,
                        "duration": round(duration, 2),
                        "success": True
                    }
                    
                    level_results.append(page_result)
                    all_results.append(page_result)
                    
                    print(f"✅ Success: '{title}' ({content_length} chars)")
                    
                    # Extract links for next depth level
                    if depth < self.max_depth:
                        new_links = await self.extract_guardian_links(result.markdown or "")
                        links_added = 0
                        for link in new_links[:5]:  # Limit links per page
                            if link not in self.crawled_urls:
                                next_level.append((link, depth + 1))
                                links_added += 1
                        
                        if links_added > 0:
                            print(f"🔗 Found {links_added} links for depth {depth + 1}")
                    
                    # Rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ Failed: {str(e)[:50]}")
                    page_result = {
                        "url": url,
                        "depth": depth,
                        "title": "Failed",
                        "content_length": 0,
                        "duration": 0,
                        "success": False,
                        "error": str(e)
                    }
                    level_results.append(page_result)
                    all_results.append(page_result)
            
            self.depth_results[depth] = level_results
            current_level = next_level
            
            print(f"📈 Depth {depth} complete: {len(level_results)} pages crawled")
        
        return {
            "max_depth_reached": max(self.depth_results.keys()) if self.depth_results else 0,
            "total_pages": len(all_results),
            "successful_pages": len([r for r in all_results if r["success"]]),
            "depth_breakdown": {d: len(results) for d, results in self.depth_results.items()},
            "results_by_depth": self.depth_results,
            "all_results": all_results
        }

async def test_depth_crawling():
    """Test true depth-based crawling"""
    print("🎯 CrawlStudio Depth-Limited Crawling Test")
    print("=" * 60)
    
    config = CrawlConfig()
    backend = FirecrawlBackend(config)  # Use fastest backend for demo
    
    # Test different depth limits
    depth_tests = [
        {"max_depth": 1, "pages_per_level": 2},
        {"max_depth": 2, "pages_per_level": 2},
        {"max_depth": 3, "pages_per_level": 1},  # Fewer pages at deeper levels
    ]
    
    guardian_home = "https://www.theguardian.com"
    
    for i, test_config in enumerate(depth_tests, 1):
        print(f"\n🧪 TEST {i}: Max Depth = {test_config['max_depth']}")
        
        crawler = DepthLimitedCrawler(
            backend, 
            max_depth=test_config['max_depth'],
            max_pages_per_level=test_config['pages_per_level']
        )
        
        result = await crawler.crawl_depth_limited(guardian_home)
        
        print(f"\n📊 DEPTH TEST {i} RESULTS:")
        print(f"🎯 Max Depth Reached: {result['max_depth_reached']}")
        print(f"📄 Total Pages: {result['total_pages']}")
        print(f"✅ Success Rate: {result['successful_pages']}/{result['total_pages']}")
        
        print(f"📈 Depth Breakdown:")
        for depth, count in result['depth_breakdown'].items():
            print(f"   Depth {depth}: {count} pages")
        
        # Show sample from each depth
        print(f"📖 Sample Results by Depth:")
        for depth, results in result['results_by_depth'].items():
            if results:
                sample = results[0]  # First result at this depth
                if sample['success']:
                    print(f"   Depth {depth}: '{sample['title'][:60]}...'")
    
    print("\n🏆 DEPTH CRAWLING CAPABILITIES SUMMARY")
    print("=" * 60)
    print("✅ TRUE DEPTH-BASED RECURSION: Fully implemented")
    print("📊 CONFIGURABLE DEPTH: 1-10+ levels possible")
    print("🎛️  PAGES PER LEVEL: Customizable limits")
    print("🔗 LINK DISCOVERY: Extracts article links at each depth")
    print("⚡ RATE LIMITING: Built-in delays for respectful crawling")
    
    print(f"\n🎯 DEPTH RECOMMENDATIONS:")
    print("• Depth 1-2: Fast overview crawling")
    print("• Depth 3-4: Comprehensive site mapping") 
    print("• Depth 5+: Deep archive crawling (use with caution)")
    print("• Reduce pages/level for deeper crawls")
    print("• Monitor crawl time (exponential growth)")

if __name__ == "__main__":
    asyncio.run(test_depth_crawling())