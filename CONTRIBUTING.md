# Contributing to CrawlStudio

Welcome to CrawlStudio! 🎉 We're building the **ultimate unified web crawling library** and aiming for **10K GitHub stars**. Your contributions are essential to making this vision a reality!

## 🚀 Vision & Mission

**Mission**: Create a unified, easy-to-use wrapper around all major web crawlers (Firecrawl, Crawl4AI, Scrapy, and future ones) with consistent APIs and excellent developer experience.

**Goal**: Reach 10,000 GitHub stars by providing the best web crawling solution in Python.

## 🏗️ Current Status

### ✅ **What's Working (80% Complete)**
- ✅ **3 Backend Integrations**: Firecrawl, Crawl4AI, Scrapy
- ✅ **Unified API**: Consistent interface across all backends
- ✅ **Single URL Scraping**: All formats (markdown, HTML, structured)
- ✅ **Comprehensive Testing**: Automated test suite
- ✅ **Cross-Platform Support**: Windows, Linux, macOS
- ✅ **Error Handling**: Robust validation and exception handling

### 🚧 **What's Needed (20% Remaining)**
- ❌ **Multi-page crawling** for all backends
- ❌ **Batch processing** capabilities
- ❌ **CLI tool** (`crawlstudio crawl website.com`)
- ❌ **URL mapping & discovery**
- ❌ **Advanced features** (proxy rotation, rate limiting)
- ❌ **Documentation** improvements

## 🛠️ How to Contribute

### 1. **Getting Started**

```bash
# Clone the repository
git clone https://github.com/aiapicore/CrawlStudio.git
cd CrawlStudio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env file
```

### 2. **Development Setup**

```bash
# Install in development mode
pip install -e .

# Run tests to ensure everything works
python tests/run_all_tests.py

# Or run individual backend tests
python simple_crawl4ai_test.py
python simple_scrapy_test.py
```

### 3. **Project Structure**

```
CrawlStudio/
├── crawlstudio/           # 📦 Main package
│   ├── backends/          # 🔧 Crawler implementations
│   ├── models.py          # 📋 Data models
│   └── utils.py           # 🛠️ Utilities
├── tests/                 # 🧪 Test suite
└── examples/              # 📖 Usage examples
```

## 🎯 Priority Contribution Areas

### 🥇 **High Priority (Needed for 10K stars)**

#### 1. **Multi-Page Crawling**
Add website crawling capabilities to all backends:

```python
# Target API
result = await backend.crawl_website(
    url="https://example.com", 
    max_pages=50, 
    depth=2
)
```

**Files to modify:**
- `crawlstudio/backends/firecrawl.py` - Add `crawl_website()` method
- `crawlstudio/backends/crawl4ai.py` - Add multi-page support  
- `crawlstudio/backends/scrapy.py` - Add depth crawling

#### 2. **CLI Tool**
Create a command-line interface:

```bash
crawlstudio crawl https://example.com --format markdown --backend firecrawl
crawlstudio batch urls.txt --output results.json
crawlstudio compare-backends https://example.com
```

**New files needed:**
- `crawlstudio/cli.py` - CLI implementation
- Update `pyproject.toml` - Entry points configuration

#### 3. **Batch Processing**
Add concurrent URL processing:

```python
# Target API  
results = await backend.crawl_batch([
    "https://site1.com",
    "https://site2.com", 
    "https://site3.com"
])
```

### 🥈 **Medium Priority**

#### 4. **Additional Backends**
Add support for more crawlers:
- **Playwright**: Browser automation
- **BeautifulSoup**: Lightweight HTML parsing
- **Selenium**: Legacy browser automation

#### 5. **Advanced Features**
- **Proxy rotation** and **IP management**
- **Rate limiting** and **throttling**
- **Retry logic** with exponential backoff
- **Caching improvements**

#### 6. **Performance Optimizations**
- **Connection pooling**
- **Async optimizations**
- **Memory management**

### 🥉 **Lower Priority**

#### 7. **Integrations**
- **LangChain** document loader
- **Streamlit** components
- **FastAPI** middleware

#### 8. **Export Options**
- **Database integrations** (MongoDB, PostgreSQL)
- **Cloud storage** (S3, GCS)
- **Multiple formats** (JSON, CSV, Excel)

## 🧪 Testing Guidelines

### **Running Tests**

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific backend tests
python tests/backends/test_firecrawl.py
python tests/backends/test_crawl4ai.py
python tests/backends/test_scrapy.py

# Run comparison tests
python final_backend_test.py
```

### **Writing Tests**

1. **Add tests for new features**:
   ```python
   # tests/backends/test_new_feature.py
   async def test_new_feature():
       backend = YourBackend(config)
       result = await backend.new_method()
       assert result.success
   ```

2. **Update integration tests**:
   ```python
   # tests/integration/test_backend_comparison.py
   # Add comparison tests for new features
   ```

### **Test Structure Cleanup**

**Current Issue**: We have test files scattered in the root directory from development. Help us organize:

**Root test files** (need to be moved/consolidated):
- `test_firecrawl.py` → `tests/backends/`
- `simple_*.py` → `examples/` or `tests/manual/`
- `comprehensive_test.py` → `tests/integration/`
- `final_backend_test.py` → `examples/demo.py`

## 📝 Code Style & Standards

### **Code Quality**
- **Type hints**: Use type annotations
- **Docstrings**: Document all public methods
- **Error handling**: Proper exception handling
- **Async/await**: Use async patterns consistently

### **Example Code Style**
```python
from typing import Dict, List, Optional
from .base import CrawlBackend
from ..models import CrawlResult, CrawlConfig

class NewBackend(CrawlBackend):
    """Backend for XYZ crawler."""
    
    async def crawl(self, url: str, format: str) -> CrawlResult:
        """Crawl a single URL.
        
        Args:
            url: Target URL to crawl
            format: Output format (markdown, html, structured)
            
        Returns:
            CrawlResult with extracted data
            
        Raises:
            ValueError: If crawling fails
        """
        try:
            # Implementation here
            return CrawlResult(...)
        except Exception as e:
            raise ValueError(f"Backend failed: {str(e)}")
```

## 🤝 How to Submit

### **Pull Request Process**

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper tests
4. **Update documentation** if needed
5. **Run tests**: Ensure all tests pass
6. **Commit** with clear messages: `git commit -m "Add amazing feature"`
7. **Push**: `git push origin feature/amazing-feature`
8. **Submit PR** with detailed description

### **PR Requirements**
- ✅ All tests must pass
- ✅ Code follows project style
- ✅ New features include tests
- ✅ Documentation updated if needed
- ✅ No breaking changes (unless discussed)

## 🏆 Recognition

### **Contributors Wall**
We'll recognize all contributors in:
- 📖 **README.md** contributors section
- 🌟 **Release notes** for major contributions
- 🎉 **Special mentions** for 10K star milestone contributors

### **Contribution Types**
- 💻 **Code contributions** (backends, features, fixes)
- 🧪 **Testing** (test cases, CI/CD, quality assurance)
- 📖 **Documentation** (guides, tutorials, API docs)
- 🐛 **Bug reports** with detailed reproduction steps
- 💡 **Feature requests** with clear use cases
- 🎨 **Design** (UI/UX for CLI, logos, branding)

## 🌟 Roadmap to 10K Stars

### **Phase 1: Foundation** (✅ Complete)
- ✅ Core backends working
- ✅ Unified API  
- ✅ Testing infrastructure

### **Phase 2: Features** (🚧 In Progress)
- 🚧 Multi-page crawling
- 🚧 CLI tool
- 🚧 Batch processing

### **Phase 3: Polish** (📅 Next)
- 📅 Advanced features
- 📅 Performance optimization
- 📅 Comprehensive docs

### **Phase 4: Ecosystem** (🔮 Future)
- 🔮 Framework integrations
- 🔮 Cloud deployment
- 🔮 Enterprise features

## 💬 Communication

### **Get Help**
- 🐛 **Bug reports**: [GitHub Issues](https://github.com/aiapicore/CrawlStudio/issues)
- 💡 **Feature requests**: [GitHub Discussions](https://github.com/aiapicore/CrawlStudio/discussions)
- ❓ **Questions**: Start a discussion or create an issue

### **Code of Conduct**
- 🤝 **Be respectful** and inclusive
- 🎯 **Focus on the mission** (10K stars goal)
- 🚀 **Be constructive** in feedback
- 📚 **Help others learn** and grow

## 🎯 Quick Start Checklist

For new contributors:

- [ ] Read this CONTRIBUTING.md
- [ ] Set up development environment
- [ ] Run existing tests successfully
- [ ] Pick an issue or feature from roadmap
- [ ] Create feature branch
- [ ] Make changes with tests
- [ ] Submit PR with clear description

## 🌟 Thank You!

Every contribution brings us closer to **10K GitHub stars** and our vision of the **best web crawling library in Python**. Whether you're fixing a bug, adding a feature, or improving documentation, you're helping developers worldwide! 

**Together, we're building something amazing!** 🎉

---

*Ready to contribute? Start by exploring our [issues](https://github.com/aiapicore/CrawlStudio/issues) or [roadmap](enhancement_suggestions.md)!*