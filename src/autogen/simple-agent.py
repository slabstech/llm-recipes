import os
from autogen import ConversableAgent

config_list = [
    {
        # Choose your model name.
        "model": "gemma:2b",
        "base_url": "http://localhost:11434/v1",
        # You need to provide your API key here.
        "api_key": "ollama",
    }
]

agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": config_list},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)

reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
print(reply)