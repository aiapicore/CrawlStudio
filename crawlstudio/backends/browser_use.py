import time
import os

from .base import CrawlBackend
from ..models import CrawlConfig, CrawlResult
from ..exceptions import DependencyMissingError, ConfigurationError, BackendExecutionError


class BrowserUseBackend(CrawlBackend):
    """
    Browser-use backend for AI-driven web automation and scraping.

    This backend uses AI agents to intelligently interact with web pages,
    making it ideal for complex scraping tasks that require understanding
    page context and performing actions.

    Requires: browser-use package and AI API key (OpenAI, Anthropic, etc.)
    """

    def __init__(self, config: CrawlConfig) -> None:
        super().__init__(config)
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check if browser-use is installed and configured."""
        try:
            import browser_use  # noqa: F401
        except ImportError:
            raise DependencyMissingError(
                "browser-use package not installed. Install with: pip install browser-use"
            )

        # Check for AI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not (openai_key or anthropic_key):
            raise ConfigurationError(
                "AI API key required for browser-use. Set OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )

    async def crawl(self, url: str, format: str) -> CrawlResult:
        """
        Crawl a URL using AI-driven browser automation.

        Args:
            url: Target URL to crawl
            format: Output format (markdown, html, structured)

        Returns:
            CrawlResult with AI-extracted data
        """
        start = time.time()

        try:
            from browser_use import Agent
            llm = self._get_llm()
            task = self._create_task(url, format)

            agent = Agent(
                task=task,
                llm=llm,
                max_actions=15,  # Allow more actions for complex pages
                use_own_browser=True,  # Use separate browser instance
            )

            result = await agent.run()

            return self._process_agent_result(url, format, result, time.time() - start)

        except Exception as e:
            raise BackendExecutionError(f"Browser-use backend error: {str(e)}")

    def _get_llm(self) -> object:
        """Get configured LLM instance."""
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if openai_key:
            try:
                from browser_use import ChatOpenAI

                class ChatOpenAIWrapper:
                    def __init__(self, model, api_key, temperature):
                        self._llm = ChatOpenAI(
                            model=model, api_key=api_key, temperature=temperature
                        )
                        # Pre-populate expected attributes
                        self.provider = "openai"
                        self.model = model
                        self.model_name = model
                        self.temperature = temperature

                    def __getattr__(self, name):
                        return getattr(self._llm, name)

                    def __setattr__(self, name, value):
                        super().__setattr__(name, value)

                    async def ainvoke(self, *args, **kwargs):
                        # Handle browser-use specific calling pattern
                        # browser-use calls: ainvoke(messages, output_format)
                        if len(args) == 2:
                            messages, output_format = args
                            if output_format:
                                kwargs['config'] = {'output_format': output_format}
                            return await self._llm.ainvoke(messages, **kwargs)
                        else:
                            return await self._llm.ainvoke(*args, **kwargs)

                    def invoke(self, *args, **kwargs):
                        return self._llm.invoke(*args, **kwargs)

                return ChatOpenAI(
                    model="gpt-4o-mini", api_key=openai_key, temperature=0
                )
            except ImportError:
                pass

        if anthropic_key:
            try:
                from browser_use import ChatAnthropic

                class ChatAnthropicWrapper:
                    def __init__(self, model, api_key, temperature):
                        self._llm = ChatAnthropic(
                            model=model, api_key=api_key, temperature=temperature
                        )
                        self.provider = "anthropic"
                        self.model = model
                        self.model_name = model
                        self.temperature = temperature

                    def __getattr__(self, name):
                        return getattr(self._llm, name)

                    def __setattr__(self, name, value):
                        super().__setattr__(name, value)

                    # Explicitly proxy key methods to ensure they work
                    async def ainvoke(self, *args, **kwargs):
                        # Handle browser-use specific calling pattern
                        # browser-use calls: ainvoke(messages, output_format)
                        if len(args) == 2:
                            messages, output_format = args
                            if output_format:
                                kwargs['config'] = {'output_format': output_format}
                            return await self._llm.ainvoke(messages, **kwargs)
                        else:
                            return await self._llm.ainvoke(*args, **kwargs)

                    def invoke(self, *args, **kwargs):
                        return self._llm.invoke(*args, **kwargs)

                return ChatAnthropic(
                    model="claude-3-haiku-20240307",  # Fast, cost-effective
                    api_key=anthropic_key,
                    temperature=0,
                )
            except ImportError:
                pass

        raise DependencyMissingError(
            "No compatible LLM library found. Install: langchain-openai or langchain-anthropic"
        )

    def _create_task(self, url: str, format: str) -> str:
        """Create AI task based on requested format."""
        if format == "markdown":
            return f"""
Go to {url} and extract the main content from the page.

Extract the following information:
- The main title/heading of the page
- All section headings (h1, h2, h3, etc.)
- The main body paragraphs with their content
- Any important lists or bullet points
- Key information tables if present

Present the information in markdown format like this:
# [Main Title]

## [Section Heading 1]
[Content of section 1...]

## [Section Heading 2]
[Content of section 2...]

Ignore navigation menus, sidebars, advertisements, and footer content.
Focus only on the main article or content body.
"""
        elif format == "html":
            return f"""
Go to {url} and extract the main content area HTML.

Find the main content section (usually within article, main, or content div tags) and return:
- The raw HTML of the main content area
- Include all HTML tags and structure
- Exclude navigation, sidebar, and footer HTML

Present the HTML code cleanly formatted.
"""
        elif format == "structured":
            return f"""
Go to {url} and extract structured information from the page.

Extract the following data:
- Page title
- Main headings and subheadings
- Key paragraphs (first 2-3 sentences of each section)
- Important links with their text and URLs
- Any data in tables or lists
- Publication date if available

Present the information in this structured format:
Title: [page title]
Headings: [list of main headings]
Content Summary: [key points from each section]
Important Links: [link text - URL]
"""
        else:
            return f"""
Go to {url} and extract the main information.

Provide a clear summary of:
- What the page is about (main topic)
- Key points or sections
- Important information or data

Present in a clear, organized format.
"""

    def _process_agent_result(
        self,
        url: str,
        format: str,
        agent_result: object,
        execution_time: float,
    ) -> CrawlResult:
        """Process agent result into CrawlResult format."""

        content = str(agent_result) if agent_result else ""

        markdown_content = None
        html_content = None
        structured_data = None

        if format == "markdown":
            markdown_content = content
        elif format == "html":
            html_content = content
        elif format == "structured":
            structured_data = {
                "title": self._extract_title(content),
                "summary": content[:500] + "..." if len(content) > 500 else content,
                "content": content,
                "keywords": self._extract_keywords(content),
            }

        metadata = {
            "ai_backend": "browser-use",
            "content_length": str(len(content)),
            "format_requested": format,
            "url": url,
        }

        return CrawlResult(
            url=url,
            backend_used="browser-use",
            markdown=markdown_content,
            raw_html=html_content,
            structured_data=structured_data,
            metadata=metadata,
            execution_time=execution_time,
            cache_hit=False,  # AI agents don't use traditional caching
        )

    def _extract_title(self, content: str) -> str:
        """Extract title from content."""
        lines = content.split("\n")
        for line in lines[:5]:  # Check first few lines
            line = line.strip()
            if line and not line.startswith("#"):
                return line[:100]  # First meaningful line as title
        return ""

    def _extract_keywords(self, content: str) -> list[str]:
        """Extract basic keywords from content."""
        # Simple keyword extraction (in production, could use AI for this too)
        words = content.lower().split()
        # Filter common words and get unique terms
        common_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
        }
        keywords = [
            word.strip('.,!?()[]{}";:')
            for word in words
            if len(word) > 3 and word not in common_words
        ]
        return list(set(keywords))[:10]  # Return top 10 unique keywords
