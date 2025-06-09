import requests
import json
from datetime import datetime

class LLMSimplifier:
    def __init__(self, api_key, base_url):
        """Initialize the LLM API client with an API key and base URL."""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.log = []  # Simple log to track requests

    def generate_text(self, prompt, max_tokens=100, temperature=0.7):
        """Generate text from a prompt with customizable parameters."""
        endpoint = f"{self.base_url}/generate"
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes
            result = response.json()
            generated_text = result.get("text", "No text returned")

            # Log the interaction
            self._log_interaction(prompt, generated_text, max_tokens, temperature)
            return generated_text

        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            self._log_interaction(prompt, error_msg, max_tokens, temperature, success=False)
            return error_msg

    def _log_interaction(self, prompt, response, max_tokens, temperature, success=True):
        """Log each API interaction for debugging or tracking."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "success": success
        }
        self.log.append(log_entry)

    def get_logs(self):
        """Return the interaction logs."""
        return self.log

    def clear_logs(self):
        """Clear the interaction logs."""
        self.log = []

 #Example main
if __name__ == "__main__":
    # Replace API key and URL
    api_key = "your-api-key-here"

    url_base = "https://api.xai.example"
    llm = LLMSimplifier(api_key, url_base)

    # Generate some text
    prompt = "Write a haiku about the moon."
    result = llm.generate_text(prompt, max_tokens=50, temperature=0.9)
    print("Generated text:", result)

    # Check the logs
    print("\nInteraction logs:")
    for entry in llm.get_logs():
        print(json.dumps(entry, indent=2))