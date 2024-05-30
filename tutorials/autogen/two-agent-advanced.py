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


work_dir = Path("groupchat")
work_dir.mkdir(exist_ok=True)

# Create Docker command line code executor.
code_executor = DockerCommandLineCodeExecutor(
    image="python:3.12-slim",  # Execute code using the given docker image name.
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=work_dir,  # Use the temporary directory to store the code files.
)


# User Proxy will execute code and finish the chat upon typing 'exit'
user_proxy = UserProxyAgent(
    name="UserProxy",
    system_message="A human admin",
    code_execution_config={
        "last_n_messages": 2,
        "executor": code_executor,
    },
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
)

# Python Coder agent
coder = AssistantAgent(
    name="softwareCoder",
    description="Software Coder, writes Python code as required and reiterates with feedback from the Code Reviewer.",
    system_message="You are a senior Python developer, a specialist in writing succinct Python functions.",
    llm_config={"config_list": config_list},
)

# Code Reviewer agent
reviewer = AssistantAgent(
    name="codeReviewer",
    description="Code Reviewer, reviews written code for correctness, efficiency, and security. Asks the Software Coder to address issues.",
    system_message="You are a Code Reviewer, experienced in checking code for correctness, efficiency, and security. Review and provide feedback to the Software Coder until you are satisfied, then return the word TERMINATE",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content"),
    llm_config={"config_list": config_list},
)

from autogen import GroupChat, GroupChatManager

# Establish the Group Chat and disallow a speaker being selected consecutively
groupchat = GroupChat(agents=[user_proxy, coder, reviewer], messages=[], max_round=12, allow_repeat_speaker=False)

# Manages the group of multiple agents
manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

from autogen.cache import Cache

# Cache LLM responses.
with Cache.disk() as cache:
    # Start the chat with a request to write a function
    user_proxy.initiate_chat(
        manager,
        message="Write a Python function for the Fibonacci sequence, the function will have one parameter for the number in the sequence, which the function will return the Fibonacci number for.",
        cache=cache,
    )
    # type exit to terminate the chat