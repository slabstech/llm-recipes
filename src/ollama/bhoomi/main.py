print("Welcome to Bhoomi")

from langchain_community.llms import Ollama

llm = Ollama(model="gemma:2b")

# test 1

# llm.invoke("Tell me a joke")

# test 2
query = "What are the top 3 important facilities required for a Robot to survive on Mars?"

query2 = "What top 5 Sensors are necessary for Robots on Mars?"

query3 = "Write a python program to connect the 5 sensors"


for chunks in llm.stream(query2):
    print(chunks)