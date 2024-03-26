from pathlib import Path
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor
import os


config_list = [
    {
        # Choose your model name.
        "model": "gemma:2b",
        "base_url": "http://localhost:11434/v1",
        # You need to provide your API key here.
        "api_key": "ollama",
    }
]

# Setting up the code executor.
workdir = Path("coding")
workdir.mkdir(exist_ok=True)
# Create a Docker command line code executor.
code_executor = DockerCommandLineCodeExecutor(
    image="python:3.12-slim",  # Execute code using the given docker image name.
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=workdir,  # Use the temporary directory to store the code files.
)


# Setting up the agents.
user_proxy_agent = UserProxyAgent(
    name="User",
    code_execution_config={"executor": code_executor},
    is_termination_msg=lambda msg: "TERMINATE" in msg.get("content"),
)

assistant_agent = AssistantAgent(
    name="Mistral Assistant",
    llm_config={"config_list": config_list},
)

chat_result = user_proxy_agent.initiate_chat(
    assistant_agent,
    message="Count how many prime numbers from 1 to 10000.",
)