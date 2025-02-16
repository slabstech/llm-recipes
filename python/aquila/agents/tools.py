"""
This module contains the tool functions used by the military decision agent system.
"""

import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.document_loaders import AssemblyAIAudioTranscriptLoader
from config import ASSEMBLYAI_API_KEY, SERPAPI_API_KEY, llm
from utils import error_handler, cache_result

@error_handler
@cache_result
def analyze_video(video_path: str) -> str:
    """
    Analyzes a video file and returns a summary of the analysis.
    
    Args:
        video_path (str): Path to the video file.
    
    Returns:
        str: A summary of the video analysis.
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    model = ResNet50(weights='imagenet', include_top=False)
    
    features = []
    for i in range(0, frame_count, 30):  # Analyze every 30th frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            img = cv2.resize(frame, (224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            features.append(model.predict(img_array).flatten())
    
    cap.release()
    
    # Here you would typically do more processing on the features
    # For this example, we'll just return a simple summary
    return f"Video analysis complete. Analyzed {len(features)} frames from {video_path}."

@error_handler
def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes an audio file using AssemblyAI.
    
    Args:
        audio_file_path (str): Path to the audio file.
    
    Returns:
        str: The transcribed text.
    """
    loader = AssemblyAIAudioTranscriptLoader(
        file_path=audio_file_path,
        api_key=ASSEMBLYAI_API_KEY
    )
    transcript = loader.load()[0]
    return transcript.page_content

@error_handler
def analyze_text(text: str) -> str:
    """
    Analyzes text data for military intelligence.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        str: A summary of the text analysis.
    """
    prompt = f"Analyze the following text for military intelligence:\n\n{text}\n\nProvide a summary of key points and potential implications."
    return llm(prompt)

# Set up the tools
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for gathering external intelligence"
    ),
    Tool(
        name="VideoAnalysis",
        func=analyze_video,
        description="Analyzes video data"
    ),
    Tool(
        name="AudioTranscription",
        func=transcribe_audio,
        description="Transcribes audio data"
    ),
    Tool(
        name="TextAnalysis",
        func=analyze_text,
        description="Analyzes text data for military intelligence"
    )
]
