"""
This module contains the configuration settings for the military decision agent system.
It loads environment variables, sets up API keys, and defines various parameters used throughout the system.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAI

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

# Environment Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# LLM Configuration
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))

# Tool Configuration
VIDEO_ANALYSIS_FRAME_RATE = int(os.getenv('VIDEO_ANALYSIS_FRAME_RATE', '1'))  # Extract 1 frame per second
MAX_FRAMES_TO_ANALYZE = int(os.getenv('MAX_FRAMES_TO_ANALYZE', '100'))
AUDIO_TRANSCRIPTION_LANGUAGE = os.getenv('AUDIO_TRANSCRIPTION_LANGUAGE', 'en')

# Agent Configuration
AGENT_VERBOSE = os.getenv('AGENT_VERBOSE', 'True').lower() == 'true'

# Security Configuration
SSL_VERIFY = os.getenv('SSL_VERIFY', 'True').lower() == 'true'
if not SSL_VERIFY:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

# Set secure file permissions
os.umask(0o077)

# Database Configuration (if applicable)
DATABASE_URL = os.getenv('DATABASE_URL')

# Caching Configuration
CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL')
CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))  # 5 minutes

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', 'military_decision_agent.log')

# Performance Configuration
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
TIMEOUT = int(os.getenv('TIMEOUT', '300'))  # 5 minutes

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=OPENAI_API_KEY, model_name=LLM_MODEL, temperature=LLM_TEMPERATURE)

# Ethical Guidelines
ETHICAL_GUIDELINES = [
    "Minimize civilian casualties",
    "Adhere to international laws of war",
    "Protect cultural and historical sites",
    "Ensure proportionality in military actions",
    "Prioritize non-violent solutions when possible"
]

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY is not set in the environment variables.")

if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY is not set in the environment variables.")

# Additional system-specific configurations can be added here

def get_config():
    """
    Returns a dictionary containing all configuration variables.
    This can be useful for debugging or logging purposes.
    """
    return {key: value for key, value in globals().items() if key.isupper()}

# You can add more configuration-related functions here if needed

