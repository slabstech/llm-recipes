import os
from typing import List, Union, Any
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain_openai import OpenAI
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Define tools
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for gathering external intelligence"
    ),
    Tool(
        name="VideoAnalysis",
        func=lambda x: "Video analysis results: " + x,
        description="Analyzes video data"
    ),
    Tool(
        name="AudioAnalysis",
        func=lambda x: "Audio analysis results: " + x,
        description="Analyzes audio data"
    ),
    Tool(
        name="TextAnalysis",
        func=lambda x: "Text analysis results: " + x,
        description="Analyzes text data"
    )
]

# Define output schemas
class PerceptionOutput(BaseModel):
    video_analysis: str = Field(description="Results of video analysis")
    audio_analysis: str = Field(description="Results of audio analysis")
    text_analysis: str = Field(description="Results of text analysis")

class IntegrationOutput(BaseModel):
    integrated_data: str = Field(description="Integrated multimodal data")

class AssessmentOutput(BaseModel):
    situation_assessment: str = Field(description="Assessment of the current situation")

class CoAOutput(BaseModel):
    courses_of_action: List[str] = Field(description="List of potential courses of action")

class EthicalEvaluationOutput(BaseModel):
    ethical_considerations: List[str] = Field(description="Ethical considerations for each course of action")

class DecisionOutput(BaseModel):
    final_decision: str = Field(description="Final decision based on all inputs and evaluations")

# Define agent class
class MilitaryAgent(LLMSingleActionAgent):
    def __init__(self, llm, tools, prompt, output_parser):
        self.llm = llm
        self.tools = tools
        self.prompt = prompt
        self.output_parser = output_parser

    def plan(self, intermediate_steps, **kwargs) -> Union[AgentAction, AgentFinish]:
        full_inputs = kwargs.copy()
        full_inputs["intermediate_steps"] = intermediate_steps
        full_inputs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        full_inputs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        
        prompt = self.prompt.format(**full_inputs)
        response = self.llm(prompt)
        
        return self.output_parser.parse(response)

    def aassign_next_action(self, output: str) -> Union[AgentAction, AgentFinish]:
        action = self.output_parser.parse(output)
        if isinstance(action, AgentAction):
            return action
        elif isinstance(action, AgentFinish):
            return action
        else:
            raise ValueError(f"Unexpected output action type: {type(action)}")

# Create agent instances
llm = OpenAI(openai_api_key=api_key)

perception_prompt = StringPromptTemplate(
    template="Analyze the following data:\n{input_data}\nUse the appropriate tools to process video, audio, and text data."
)
perception_parser = PydanticOutputParser(pydantic_object=PerceptionOutput)

integration_prompt = StringPromptTemplate(
    template="Integrate the following multimodal data:\n{perception_output}\nProvide a cohesive summary of the integrated information."
)
integration_parser = PydanticOutputParser(pydantic_object=IntegrationOutput)

assessment_prompt = StringPromptTemplate(
    template="Assess the following situation based on the integrated data:\n{integration_output}\nProvide a comprehensive situation assessment."
)
assessment_parser = PydanticOutputParser(pydantic_object=AssessmentOutput)

coa_prompt = StringPromptTemplate(
    template="Generate potential courses of action based on the following situation assessment:\n{assessment_output}\nList multiple viable options."
)
coa_parser = PydanticOutputParser(pydantic_object=CoAOutput)

ethical_prompt = StringPromptTemplate(
    template="Evaluate the ethical considerations for each of the following courses of action:\n{coa_output}\nProvide ethical analysis for each option."
)
ethical_parser = PydanticOutputParser(pydantic_object=EthicalEvaluationOutput)

decision_prompt = StringPromptTemplate(
    template="Formulate a final decision based on the following ethical evaluation:\n{ethical_output}\nProvide a clear and justified decision."
)
decision_parser = PydanticOutputParser(pydantic_object=DecisionOutput)

perception_agent = MilitaryAgent(llm, tools, perception_prompt, perception_parser)
integration_agent = MilitaryAgent(llm, tools, integration_prompt, integration_parser)
situation_assessment_agent = MilitaryAgent(llm, tools, assessment_prompt, assessment_parser)
course_of_action_agent = MilitaryAgent(llm, tools, coa_prompt, coa_parser)
ethical_evaluation_agent = MilitaryAgent(llm, tools, ethical_prompt, ethical_parser)
decision_output_agent = MilitaryAgent(llm, tools, decision_prompt, decision_parser)

# Set up agent executors
perception_executor = AgentExecutor.from_agent_and_tools(
    agent=perception_agent,
    tools=tools,
    verbose=True
)

integration_executor = AgentExecutor.from_agent_and_tools(
    agent=integration_agent,
    tools=tools,
    verbose=True
)

assessment_executor = AgentExecutor.from_agent_and_tools(
    agent=situation_assessment_agent,
    tools=tools,
    verbose=True
)

coa_executor = AgentExecutor.from_agent_and_tools(
    agent=course_of_action_agent,
    tools=tools,
    verbose=True
)

ethical_executor = AgentExecutor.from_agent_and_tools(
    agent=ethical_evaluation_agent,
    tools=tools,
    verbose=True
)

decision_executor = AgentExecutor.from_agent_and_tools(
    agent=decision_output_agent,
    tools=tools,
    verbose=True
)

# Implement agent coordination
def coordinate_agents(input_data: str) -> str:
    perception_result = perception_executor.run(input_data=input_data)
    integration_result = integration_executor.run(perception_output=perception_result)
    assessment_result = assessment_executor.run(integration_output=integration_result)
    coa_result = coa_executor.run(assessment_output=assessment_result)
    ethical_result = ethical_executor.run(coa_output=coa_result)
    final_decision = decision_executor.run(ethical_output=ethical_result)
    return final_decision

# Run the system
if __name__ == "__main__":
    military_input = """
    Analyze the following:
    1. Video feed showing troop movements in sector A5
    2. Audio intercepts of enemy communications
    3. Text reports from field agents
    Provide a comprehensive decision based on this data.
    """
    final_decision = coordinate_agents(military_input)
    print("Final Decision:")
    print(final_decision)
