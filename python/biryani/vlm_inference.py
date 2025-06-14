from openai import OpenAI

# Set your custom endpoint and API key
client = OpenAI(
    api_key="lerobot@hf.co_dwani_lebot",
    base_url="some_key"  # Ensure /v1 is included if your endpoint expects it
)

response = client.chat.completions.create(
    model="gpt-4o",  # Or your supported model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                    }
                }
            ]
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)
