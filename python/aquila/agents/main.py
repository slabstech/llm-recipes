"""
This module contains the main execution logic for the military decision agent system.
It coordinates the different agents to process input data and produce a final decision.
"""

import asyncio
import logging
from pydantic import BaseModel, validator
import os
from typing import List

from agents import (
    perception_executor, integration_executor, assessment_executor,
    coa_executor, ethical_executor, decision_executor
)
from config import DEBUG
from utils import error_handler

# Set up logging
logging.basicConfig(level=logging.INFO if DEBUG else logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MilitaryInput(BaseModel):
    video_path: str
    audio_path: str
    text_report: str

    @validator('video_path', 'audio_path')
    def file_exists(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")
        return v

    @validator('text_report')
    def non_empty_text(cls, v):
        if not v.strip():
            raise ValueError("Text report cannot be empty")
        return v

class MilitaryOutput(BaseModel):
    final_decision: str
    courses_of_action: List[str]
    ethical_considerations: List[str]

@error_handler
async def async_coordinate_agents(input_data: MilitaryInput) -> MilitaryOutput:
    """
    Coordinates the execution of all agents in the military decision system.

    Args:
        input_data (MilitaryInput): The input data containing paths to video, audio, and text report.

    Returns:
        MilitaryOutput: The final decision, courses of action, and ethical considerations.
    """
    logger.info("Starting agent coordination")
    
    perception_result = await perception_executor.arun(input_data=input_data.dict())
    logger.info("Perception analysis complete")
    
    integration_result = await integration_executor.arun(perception_output=perception_result)
    logger.info("Data integration complete")
    
    assessment_result = await assessment_executor.arun(integration_output=integration_result)
    logger.info("Situation assessment complete")
    
    coa_result = await coa_executor.arun(assessment_output=assessment_result)
    logger.info("Courses of action generated")
    
    ethical_result = await ethical_executor.arun(coa_output=coa_result)
    logger.info("Ethical evaluation complete")
    
    final_decision = await decision_executor.arun(ethical_output=ethical_result)
    logger.info("Final decision formulated")

    return MilitaryOutput(
        final_decision=final_decision,
        courses_of_action=coa_result.courses_of_action,
        ethical_considerations=ethical_result.ethical_considerations
    )

@error_handler
async def process_military_input(video_path: str, audio_path: str, text_report: str) -> MilitaryOutput:
    """
    Processes the military input and returns the final output.

    Args:
        video_path (str): Path to the video file.
        audio_path (str): Path to the audio file.
        text_report (str): The text report.

    Returns:
        MilitaryOutput: The final decision, courses of action, and ethical considerations.
    """
    try:
        military_input_data = MilitaryInput(
            video_path=video_path,
            audio_path=audio_path,
            text_report=text_report
        )
    except ValueError as e:
        logger.error(f"Invalid input data: {str(e)}")
        raise

    return await async_coordinate_agents(military_input_data)

async def main():
    """
    Main function to run the military decision agent system.
    """
    video_path = "/path/to/video/feed.mp4"
    audio_path = "/path/to/audio/intercepts.wav"
    text_report = """
    Enemy forces spotted moving towards sector B7. 
    Estimated strength: 100 personnel, 5 armored vehicles.
    """

    try:
        result = await process_military_input(video_path, audio_path, text_report)
        print("Final Decision:")
        print(result.final_decision)
        print("\nCourses of Action:")
        for coa in result.courses_of_action:
            print(f"- {coa}")
        print("\nEthical Considerations:")
        for consideration in result.ethical_considerations:
            print(f"- {consideration}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
