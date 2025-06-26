from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
      {
        "role": "user",
        "content": "hello"
      },
      {
        "role": "assistant",
        "content": "Hello! It's nice to meet you. Is there something I can help you with or would you like to chat?"
      },
      {
        "role": "user",
        "content": "what is this ?\n"
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
