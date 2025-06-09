import openai
import logging
import time
import backoff
from typing import Optional, Dict, List, Generator
from ratelimit import limits, sleep_and_retry

class LLMSimplifier:
    def __init__(self, api_key: str, provider: str = "openai",
                 temperature: float = 0.7, max_tokens: int = 512,
                 log_file: str = "llm_api.log"):
        """Initialize the LLM API client with an API key, provider, and parameters."""
        self.provider = provider.lower()
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._setup_logging(log_file)
        self._setup_client()
        self.call_count = 0
        self.rate_limit_period = 60  # seconds
        self.rate_limit_calls = 50   # calls per period

    def _setup_logging(self, log_file: str) -> None:
        """Configure file-based logging for API interactions."""
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized LLMSimplifier for {self.provider}")

    def _setup_client(self) -> None:
        """Set up the API client based on the provider."""
        if self.provider == "openai":
            openai.api_key = self.api_key
            self.client = openai
        elif self.provider == "xai":
            # Placeholder for xAI client setup
            self.client = None  # Configure xAI API client
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    @backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.APIError), max_tries=3)
    @sleep_and_retry
    @limits(calls=50, period=60)
    def generate_text(self, prompt: str,
                     temperature: Optional[float] = None,
                     max_tokens: Optional[int] = None) -> str:
        """Generate text from a prompt with customizable parameters."""
        self.call_count += 1
        params = {
            "model": "gpt-4" if self.provider == "openai" else "grok-3",
            "prompt": prompt,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }
        try:
            self.logger.info(f"Sending request {self.call_count}: {prompt[:50]}...")
            response = self.client.Completion.create(**params)
            text = response.choices[0].text.strip()
            self.logger.info(f"Received response for request {self.call_count}")
            return text
        except Exception as e:
            self.logger.error(f"Error in request {self.call_count}: {str(e)}")
            raise

    @sleep_and_retry
    @limits(calls=50, period=60)
    def batch_generate(self, prompts: List[str],
                      temperature: Optional[float] = None,
                      max_tokens: Optional[int] = None) -> List[str]:
        """Process multiple prompts in a batch, respecting rate limits."""
        results = []
        self.logger.info(f"Starting batch processing for {len(prompts)} prompts")
        for i, prompt in enumerate(prompts, 1):
            try:
                result = self.generate_text(prompt, temperature, max_tokens)
                results.append(result)
                self.logger.info(f"Completed prompt {i}/{len(prompts)}")
            except Exception as e:
                self.logger.error(f"Failed prompt {i}: {str(e)}")
                results.append(f"Error: {str(e)}")
        self.logger.info(f"Finished batch processing: {len(results)} results")
        return results

    def stream_text(self, prompt: str,
                    temperature: Optional[float] = None,
                    max_tokens: Optional[int] = None) -> Generator[str, None, None]:
        """Handle streaming responses for real-time applications."""
        self.call_count += 1
        params = {
            "model": "gpt-4" if self.provider == "openai" else "grok-3",
            "prompt": prompt,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "stream": True if self.provider == "openai" else False
        }
        try:
            self.logger.info(f"Streaming request {self.call_count}: {prompt[:50]}...")
            if self.provider == "openai":
                response = self.client.Completion.create(**params)
                for chunk in response:
                    if chunk.choices and chunk.choices[0].text:
                        text = chunk.choices[0].text.strip()
                        self.logger.info(f"Received stream chunk for request {self.call_count}")
                        yield text
            else:
                # Fallback to non-streaming for unsupported providers
                text = self.generate_text(prompt, temperature, max_tokens)
                self.logger.info(f"Non-streaming fallback for request {self.call_count}")
                yield text
        except Exception as e:
            self.logger.error(f"Error in streaming request {self.call_count}: {str(e)}")
            raise