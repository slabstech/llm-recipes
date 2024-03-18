import json

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

json_schema = {
    "title": "Person",
    "description": "Identifying information about a person.",
    "type": "object",
    "properties": {
        "name": {"title": "Name", "description": "The person's name", "type": "string"},
        "age": {"title": "Age", "description": "The person's age", "type": "integer"},
        "fav_food": {
            "title": "Fav Food",
            "description": "The person's favorite food",
            "type": "string",
        },
    },
    "required": ["name", "age"],
}

llm = ChatOllama(model="gemma:2b")

messages = [
    HumanMessage(
        content="Please tell me about a person using the following JSON schema:"
    ),
    HumanMessage(content="{dumps}"),
    HumanMessage(
        content="Now, considering the schema, tell me about a person named Sachin who is 32 years old and loves Biryani."
    ),
]

prompt = ChatPromptTemplate.from_messages(messages)
dumps = json.dumps(json_schema, indent=2)

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"dumps": dumps}))