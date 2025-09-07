import asyncio
from crawlstudio import CrawlConfig, FirecrawlBackend, Crawl4AIBackend, ScrapyBackend

async def main():
    config = CrawlConfig()
    
    # Different backends - uncomment to test
    # backend = FirecrawlBackend(config)
    backend = Crawl4AIBackend(config)
    # backend = ScrapyBackend(config)
    
    # Different formats - uncomment to test  
    #result = await backend.crawl("https://www.wtatennis.com/rankings/singles", format="markdown")
    result = await backend.crawl("https://www.wtatennis.com/rankings/singles", format="html")
    #result = await backend.crawl("https://www.wtatennis.com/rankings/singles", format="structured")
    
    # Different outputs - uncomment to test
    print(result.markdown)
    #print(result.raw_html)
    #print(result.structured_data)

asyncio.run(main())