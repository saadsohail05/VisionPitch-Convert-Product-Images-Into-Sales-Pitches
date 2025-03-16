from together import Together
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your API key
api_key = os.getenv('TOGETHER_API_KEY')
if not api_key:
    print("Error: TOGETHER_API_KEY not found in .env file")
    exit(1)

# Initialize the client
Together.api_key = api_key

# Add a simple test message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a short joke."}
]

response = Together().chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=messages,
    max_tokens=None,
    temperature=0.5,
    top_p=0.5,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>","<|eom_id|>"],
    stream=True
)

for token in response:
    if hasattr(token, 'choices'):
        print(token.choices[0].delta.content, end='', flush=True)