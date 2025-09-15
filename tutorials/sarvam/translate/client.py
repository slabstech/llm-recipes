from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id


tgt_lang = 'Hindi'

tgt_lang = 'kannada'

input_txt = 'Be the change you wish to see in the world.'

input_txt = 'Towards a new century of nation building, Bharat 2047.'
messages = [{"role": "system", "content": f"Translate the text below to {tgt_lang}."}, {"role": "user", "content": input_txt}]


response = client.chat.completions.create(model=model, messages=messages, temperature=0.01)
output_text = response.choices[0].message.content

print("Input:", input_txt)
print("Translation:", output_text)
