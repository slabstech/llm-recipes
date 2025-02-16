"""
This module defines the Pydantic models used for data validation and serialization
in the military decision agent system.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class VideoAnalysisResult(BaseModel):
    """Model for video analysis results."""
    frame_count: int = Field(..., description="Number of frames analyzed")
    detected_objects: List[str] = Field(..., description="List of objects detected in the video")
    movement_patterns: str = Field(..., description="Description of observed movement patterns")
    key_events: List[str] = Field(..., description="List of key events identified in the video")

class AudioAnalysisResult(BaseModel):
    """Model for audio analysis results."""
    transcript: str = Field(..., description="Transcription of the audio content")
    speaker_count: int = Field(..., description="Estimated number of distinct speakers")
    key_phrases: List[str] = Field(..., description="List of key phrases identified in the audio")
    sentiment: str = Field(..., description="Overall sentiment of the audio content")

class TextAnalysisResult(BaseModel):
    """Model for text analysis results."""
    summary: str = Field(..., description="Summary of the text content")
    entities: List[str] = Field(..., description="List of entities mentioned in the text")
    key_points: List[str] = Field(..., description="List of key points extracted from the text")
    sentiment: str = Field(..., description="Sentiment analysis of the text")

class PerceptionOutput(BaseModel):
    """Model for the output of the perception stage."""
    video_analysis: VideoAnalysisResult = Field(..., description="Results of video analysis")
    audio_analysis: AudioAnalysisResult = Field(..., description="Results of audio analysis")
    text_analysis: TextAnalysisResult = Field(..., description="Results of text analysis")

class IntegrationOutput(BaseModel):
    """Model for the output of the integration stage."""
    integrated_summary: str = Field(..., description="Integrated summary of all analyzed data")
    key_insights: List[str] = Field(..., description="List of key insights from the integrated data")
    potential_threats: List[str] = Field(..., description="List of potential threats identified")
    information_gaps: List[str] = Field(..., description="List of identified information gaps")

class SituationFactor(BaseModel):
    """Model for individual situation factors."""
    factor: str = Field(..., description="Description of the factor")
    impact: str = Field(..., description="Potential impact of the factor")
    certainty: float = Field(..., ge=0, le=1, description="Certainty level of the factor (0-1)")

class AssessmentOutput(BaseModel):
    """Model for the output of the situation assessment stage."""
    current_situation: str = Field(..., description="Description of the current situation")
    critical_factors: List[SituationFactor] = Field(..., description="List of critical factors affecting the situation")
    potential_developments: List[str] = Field(..., description="List of potential future developments")
    overall_threat_level: str = Field(..., description="Assessment of the overall threat level")

class CourseOfAction(BaseModel):
    """Model for individual courses of action."""
    action: str = Field(..., description="Description of the proposed action")
    objectives: List[str] = Field(..., description="List of objectives this action aims to achieve")
    resources_required: List[str] = Field(..., description="List of resources required for this action")
    risks: List[str] = Field(..., description="List of potential risks associated with this action")
    benefits: List[str] = Field(..., description="List of potential benefits of this action")
    timeline: str = Field(..., description="Estimated timeline for this action")

class CoAOutput(BaseModel):
    """Model for the output of the course of action generation stage."""
    courses_of_action: List[CourseOfAction] = Field(..., description="List of potential courses of action")
    recommended_coa: Optional[str] = Field(None, description="Recommended course of action, if any")

class EthicalConsideration(BaseModel):
    """Model for individual ethical considerations."""
    consideration: str = Field(..., description="Description of the ethical consideration")
    related_coa: str = Field(..., description="The course of action this consideration relates to")
    potential_impact: str = Field(..., description="Potential ethical impact")
    mitigation_strategies: List[str] = Field(..., description="Possible strategies to mitigate ethical concerns")

class EthicalEvaluationOutput(BaseModel):
    """Model for the output of the ethical evaluation stage."""
    ethical_considerations: List[EthicalConsideration] = Field(..., description="List of ethical considerations for each course of action")
    overall_ethical_assessment: str = Field(..., description="Overall ethical assessment of the situation and proposed actions")

class DecisionOutput(BaseModel):
    """Model for the final decision output."""
    chosen_action: str = Field(..., description="The chosen course of action")
    rationale: str = Field(..., description="Rationale for the decision")
    key_considerations: List[str] = Field(..., description="Key considerations that influenced the decision")
    implementation_steps: List[str] = Field(..., description="Steps for implementing the decision")
    contingency_plans: List[str] = Field(..., description="Contingency plans in case of unforeseen circumstances")

class MilitaryMissionInput(BaseModel):
    """Model for the initial military mission input."""
    mission_type: str = Field(..., description="Type of military mission")
    location: str = Field(..., description="Location of the mission")
    time_frame: str = Field(..., description="Time frame for the mission")
    available_resources: List[str] = Field(..., description="List of available resources")
    intelligence_summary: str = Field(..., description="Summary of available intelligence")
    mission_objectives: List[str] = Field(..., description="List of mission objectives")

class MilitaryMissionOutput(BaseModel):
    """Model for the complete military mission output."""
    mission_input: MilitaryMissionInput = Field(..., description="The initial mission input")
    perception: PerceptionOutput = Field(..., description="Results of the perception stage")
    integration: IntegrationOutput = Field(..., description="Results of the integration stage")
    assessment: AssessmentOutput = Field(..., description="Results of the situation assessment stage")
    courses_of_action: CoAOutput = Field(..., description="Generated courses of action")
    ethical_evaluation: EthicalEvaluationOutput = Field(..., description="Ethical evaluation of courses of action")
    final_decision: DecisionOutput = Field(..., description="The final decision and implementation plan")
