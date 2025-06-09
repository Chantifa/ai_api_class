# LLMSimplifier: Simplifying Large Language Model API Interactions

LLMSimplifier is a Python package designed to streamline interactions with large language model (LLM) APIs, such as OpenAI and xAI, by abstracting complexities like rate limits, parameter tuning, and error handling. Using object-oriented principles, it provides a unified interface with methods for text generation, batch processing, and streaming responses, making it ideal for applications like chatbots, content generation, and sentiment analysis.

## Features

- **Simplified API Calls**: Use methods like `generate_text`, `batch_generate`, and `stream_text` for easy interaction.
- **Rate Limit Handling**: Implements exponential backoff and request throttling to manage HTTP 429 errors.
- **Flexible Parameters**: Adjust `temperature` and `max_tokens` for task-specific outputs (e.g., creative writing or summarization).
- **Logging**: Tracks API interactions and errors for debugging and compliance.
- **Multi-Provider Support**: Configurable for OpenAI and placeholder for xAI (extensible to other providers).
- **Batch Processing**: Efficiently processes multiple prompts for high-throughput tasks.
- **Streaming Support**: Handles real-time responses for interactive applications like chatbots.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Chantifa/ai_api_class.git