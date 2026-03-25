"""
LLM Gateway: Centralized LLM access for all SAGA agents.

All agents call this instead of directly importing Gemini or Ollama.
When Ollama is ready, just uncomment the config in config.py and add
an if-branch here — zero changes needed in any agent code.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import GEMINI_API_KEY, GEMINI_FAST_MODEL, GEMINI_POWER_MODEL

# Future: from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class LLMGateway:
    """
    Centralized LLM provider. Currently Gemini-only.
    Swap in Ollama later by uncommenting config and adding an if-branch.
    """

    @staticmethod
    def get_fast_llm() -> ChatGoogleGenerativeAI:
        """
        Returns the fast model for routing/classification.
        Currently: Gemini Flash (~500ms).
        Future: Ollama local model (~150ms).
        """
        # Future Ollama swap-in:
        # if OLLAMA_BASE_URL:
        #     from langchain_community.chat_models import ChatOllama
        #     return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

        return ChatGoogleGenerativeAI(
            model=GEMINI_FAST_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.0,
            max_output_tokens=50,  # Classification needs very few tokens
        )

    @staticmethod
    def get_power_llm() -> ChatGoogleGenerativeAI:
        """
        Returns the powerful model for code generation and deep analysis.
        Currently: Gemini Pro.
        """
        return ChatGoogleGenerativeAI(
            model=GEMINI_POWER_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.2,
            max_output_tokens=4096,
        )
