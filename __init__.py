from llm_simplifier import LLMSimplifier

# Initialize with API key and provider
llm = LLMSimplifier(api_key="your-api-key-here", provider="openai")

# Generate text
prompt = "Write a haiku about the moon."
result = llm.generate_text(prompt, temperature=0.9, max_tokens=50)
print("Generated text:", result)

# Batch Processing
prompts = ["Write a haiku about the sun.", "Summarize AI history in 50 words."]
results = llm.batch_generate(prompts, temperature=0.7, max_tokens=100)
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}\nResult: {result}\n")

# Streaming Responses
prompt = "Tell a short story."
for chunk in llm.stream_text(prompt, temperature=0.8, max_tokens=200):
    print(chunk, end="", flush=True)