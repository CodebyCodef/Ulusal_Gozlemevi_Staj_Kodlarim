import requests
import json

API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps({
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": "How many r's are in the word 'strawberry'?"}
        ],
        "reasoning": {"enabled": True}
    })
)

response = response.json()
response = response['choices'][0]['message']

messages = [
    {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
    {
        "role": "assistant",
        "content": response.get('content'),
    },
    {"role": "user", "content": "Are you sure? Think carefully."}
]

response2 = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    data=json.dumps({
        "model": "openrouter/free",
        "messages": messages,
        "reasoning": {"enabled": True}
    })
)

print("=== First Response ===")
print(response.get('content'))
print("\n=== Second Response ===")
print(response2.json()['choices'][0]['message']['content'])
