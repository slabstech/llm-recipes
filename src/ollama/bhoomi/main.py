print("Welcome to Bhoomi")

from langchain_community.llms import Ollama

llm = Ollama(model="mistral")

# test 1

# llm.invoke("Tell me a joke")

# test 2
query = "Tell me a joke"

for chunks in llm.stream(query):
    print(chunks)