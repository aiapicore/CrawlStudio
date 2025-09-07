"""
Simple test for Browser-Use backend
Note: Requires browser-use package and AI API key
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_browser_use():
    print("Testing Browser-Use backend...")
    print("="*50)
    
    # Check if dependencies are available
    try:
        import browser_use
        print("✓ browser-use package installed")
    except ImportError:
        print("✗ browser-use package not found")
        print("Install with: pip install browser-use")
        print("Then run: uvx playwright install chromium --with-deps")
        return
    
    # Check for AI API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not (openai_key or anthropic_key):
        print("✗ No AI API key found")
        print("Add to .env file:")
        print("OPENAI_API_KEY=your_key_here")
        print("or")
        print("ANTHROPIC_API_KEY=your_key_here")
        return
    
    print(f"✓ AI API key available ({'OpenAI' if openai_key else 'Anthropic'})")
    
    try:
        from crawlstudio import CrawlConfig, BrowserUseBackend
        
        config = CrawlConfig()
        backend = BrowserUseBackend(config)
        
        print("\n🤖 Testing AI-driven web scraping...")
        print("Note: This may take longer as it uses AI agents")
        
        # Test simple page
        result = await backend.crawl("https://httpbin.org/html", format="structured")
        
        print(f"\n✓ SUCCESS: {result.backend_used}")
        print(f"⏱️  Execution: {result.execution_time:.2f}s")
        print(f"🧠 AI Backend: {result.metadata.get('ai_backend', 'N/A')}")
        
        if result.structured_data:
            print(f"📝 Title: {result.structured_data.get('title', 'N/A')[:50]}...")
            print(f"📊 Keywords: {len(result.structured_data.get('keywords', []))} found")
            print(f"📄 Content: {len(result.structured_data.get('content', ''))} chars")
        
        print("\n🎉 Browser-Use backend working with AI!")
        print("This backend can handle complex web interactions that require AI understanding.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "browser-use" in str(e):
            print("💡 Install browser-use: pip install browser-use")
        elif "API key" in str(e):
            print("💡 Add AI API key to .env file")
        elif "langchain" in str(e):
            print("💡 Install LangChain: pip install langchain-openai")


if __name__ == "__main__":
    asyncio.run(test_browser_use())