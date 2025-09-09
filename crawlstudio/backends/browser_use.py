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
            # Import browser-use components
            from browser_use import Agent

            # Try to import LLM - prefer OpenAI, fallback to others
            llm = self._get_llm()

            # Create task based on format requested
            task = self._create_task(url, format)

            # Create and run agent
            agent = Agent(
                task=task,
                llm=llm,
                max_actions=10,  # Limit actions to prevent runaway
                use_own_browser=True  # Use separate browser instance
            )

            # Run the agent and get result
            result = await agent.run()

            # Process the agent result into our format
            return self._process_agent_result(url, format, result, time.time() - start)

        except Exception as e:
            raise BackendExecutionError(f"Browser-use backend error: {str(e)}")

    def _get_llm(self) -> object:
        """Get configured LLM instance."""
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if openai_key:
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model="gpt-4o-mini",  # Cost-effective model
                    api_key=openai_key,
                    temperature=0
                )
            except ImportError:
                pass

        if anthropic_key:
            try:
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model="claude-3-haiku-20240307",  # Fast, cost-effective
                    api_key=anthropic_key,
                    temperature=0
                )
            except ImportError:
                pass

        raise DependencyMissingError(
            "No compatible LLM library found. Install: langchain-openai or langchain-anthropic"
        )

    def _create_task(self, url: str, format: str) -> str:
        """Create AI task based on requested format."""
        base_task = f"Navigate to {url} and extract content"

        if format == "markdown":
            return (
                f"{base_task}. Convert the main content to markdown format, "
                f"preserving structure with headers, paragraphs, and lists. "
                f"Focus on the primary text content, ignoring navigation and ads."
            )
        elif format == "html":
            return (
                f"{base_task}. Extract the raw HTML source of the main content area. "
                f"Include the HTML tags and structure."
            )
        elif format == "structured":
            return (
                f"{base_task}. Extract structured information including: "
                f"page title, main headings, key paragraphs, important links, "
                f"and any data tables. Format as a structured summary."
            )
        else:
            return f"{base_task}. Summarize the main content and key information."

    def _process_agent_result(
        self,
        url: str,
        format: str,
        agent_result: object,
        execution_time: float,
    ) -> CrawlResult:
        """Process agent result into CrawlResult format."""

        # Extract text content from agent result
        content = str(agent_result) if agent_result else ""

        # Process based on format
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
                "keywords": self._extract_keywords(content)
            }

        # Create metadata
        metadata = {
            "ai_backend": "browser-use",
            "content_length": str(len(content)),
            "format_requested": format,
            "url": url
        }

        return CrawlResult(
            url=url,
            backend_used="browser-use",
            markdown=markdown_content,
            raw_html=html_content,
            structured_data=structured_data,
            metadata=metadata,
            execution_time=execution_time,
            cache_hit=False  # AI agents don't use traditional caching
        )

    def _extract_title(self, content: str) -> str:
        """Extract title from content."""
        lines = content.split('\n')
        for line in lines[:5]:  # Check first few lines
            line = line.strip()
            if line and not line.startswith('#'):
                return line[:100]  # First meaningful line as title
        return ""

    def _extract_keywords(self, content: str) -> list[str]:
        """Extract basic keywords from content."""
        # Simple keyword extraction (in production, could use AI for this too)
        words = content.lower().split()
        # Filter common words and get unique terms
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at',
                        'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        keywords = [word.strip('.,!?()[]{}";:') for word in words
                    if len(word) > 3 and word not in common_words]
        return list(set(keywords))[:10]  # Return top 10 unique keywords
