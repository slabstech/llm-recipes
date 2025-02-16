"""
This module defines the MilitaryAgent class and sets up all agent instances
for the military decision agent system.
"""

from typing import Union, List, Dict, Any
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from config import llm, tools, AGENT_VERBOSE
from models import (
    PerceptionOutput, IntegrationOutput, AssessmentOutput,
    CoAOutput, EthicalEvaluationOutput, DecisionOutput
)
from utils import error_handler

class MilitaryAgent(LLMSingleActionAgent):
    """
    A custom agent class for military decision-making tasks.
    """

    def __init__(self, llm, tools: List[Any], prompt: StringPromptTemplate, output_parser: PydanticOutputParser):
        self.llm = llm
        self.tools = tools
        self.prompt = prompt
        self.output_parser = output_parser

    @error_handler
    def plan(self, intermediate_steps: List[tuple], **kwargs: Dict[str, Any]) -> Union[AgentAction, AgentFinish]:
        """
        Plan the next action based on the current state and intermediate steps.

        Args:
            intermediate_steps (List[tuple]): List of previous actions and their results.
            **kwargs: Additional keyword arguments.

        Returns:
            Union[AgentAction, AgentFinish]: The next action to take or the final result.
        """
        full_inputs = kwargs.copy()
        full_inputs["intermediate_steps"] = intermediate_steps
        full_inputs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        full_inputs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        
        prompt = self.prompt.format(**full_inputs)
        response = self.llm(prompt)
        
        return self.output_parser.parse(response)

    @error_handler
    def aassign_next_action(self, output: str) -> Union[AgentAction, AgentFinish]:
        """
        Assign the next action based on the output of the language model.

        Args:
            output (str): The output from the language model.

        Returns:
            Union[AgentAction, AgentFinish]: The next action to take or the final result.
        """
        action = self.output_parser.parse(output)
        if isinstance(action, AgentAction):
            return action
        elif isinstance(action, AgentFinish):
            return action
        else:
            raise ValueError(f"Unexpected output action type: {type(action)}")

# Define prompts for each agent
perception_prompt = StringPromptTemplate(
    template="""Analyze the following data:
    Video: {video_data}
    Audio: {audio_data}
    Text: {text_data}
    
    Use the appropriate tools to process video, audio, and text data.
    Provide a comprehensive analysis of the perceived information.
    """
)

integration_prompt = StringPromptTemplate(
    template="""Integrate the following multimodal data:
    {perception_output}
    
    Provide a cohesive summary of the integrated information, highlighting key insights and potential implications.
    """
)

assessment_prompt = StringPromptTemplate(
    template="""Assess the following situation based on the integrated data:
    {integration_output}
    
    Provide a comprehensive situation assessment, including:
    1. Current state of affairs
    2. Potential threats and opportunities
    3. Critical factors influencing the situation
    """
)

coa_prompt = StringPromptTemplate(
    template="""Generate potential courses of action based on the following situation assessment:
    {assessment_output}
    
    List multiple viable options, considering:
    1. Strategic objectives
    2. Available resources
    3. Potential risks and benefits
    4. Time constraints
    """
)

ethical_prompt = StringPromptTemplate(
    template="""Evaluate the ethical considerations for each of the following courses of action:
    {coa_output}
    
    Provide ethical analysis for each option, considering:
    1. Adherence to international laws and conventions
    2. Potential civilian impact
    3. Long-term consequences
    4. Alignment with military ethics and values
    """
)

decision_prompt = StringPromptTemplate(
    template="""Formulate a final decision based on the following ethical evaluation:
    {ethical_output}
    
    Provide a clear and justified decision, including:
    1. Chosen course of action
    2. Rationale for the decision
    3. Key considerations and trade-offs
    4. Implementation guidelines
    """
)

# Create agent instances
perception_agent = MilitaryAgent(llm, tools, perception_prompt, PydanticOutputParser(pydantic_object=PerceptionOutput))
integration_agent = MilitaryAgent(llm, tools, integration_prompt, PydanticOutputParser(pydantic_object=IntegrationOutput))
situation_assessment_agent = MilitaryAgent(llm, tools, assessment_prompt, PydanticOutputParser(pydantic_object=AssessmentOutput))
course_of_action_agent = MilitaryAgent(llm, tools, coa_prompt, PydanticOutputParser(pydantic_object=CoAOutput))
ethical_evaluation_agent = MilitaryAgent(llm, tools, ethical_prompt, PydanticOutputParser(pydantic_object=EthicalEvaluationOutput))
decision_output_agent = MilitaryAgent(llm, tools, decision_prompt, PydanticOutputParser(pydantic_object=DecisionOutput))

# Set up agent executors
perception_executor = AgentExecutor.from_agent_and_tools(agent=perception_agent, tools=tools, verbose=AGENT_VERBOSE)
integration_executor = AgentExecutor.from_agent_and_tools(agent=integration_agent, tools=tools, verbose=AGENT_VERBOSE)
assessment_executor = AgentExecutor.from_agent_and_tools(agent=situation_assessment_agent, tools=tools, verbose=AGENT_VERBOSE)
coa_executor = AgentExecutor.from_agent_and_tools(agent=course_of_action_agent, tools=tools, verbose=AGENT_VERBOSE)
ethical_executor = AgentExecutor.from_agent_and_tools(agent=ethical_evaluation_agent, tools=tools, verbose=AGENT_VERBOSE)
decision_executor = AgentExecutor.from_agent_and_tools(agent=decision_output_agent, tools=tools, verbose=AGENT_VERBOSE)
