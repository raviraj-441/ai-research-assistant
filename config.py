# Configuration settings and constants
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model Configuration
GROQ_MODEL_NAME = "mixtral-8x7b-32768"
GROQ_TEMPERATURE = 0

# Token Usage Control
MAX_SOURCES_IN_PROMPT = 5
SOURCE_CHAR_LIMIT_DRAFT = 200      # For answer drafting
SOURCE_CHAR_LIMIT_FACTCHECK = 200  # For fact-checking prompt
SOURCE_CHAR_LIMIT_VALIDATION = 150 # For final validation prompt
SOURCE_CHAR_LIMIT_REPORT = 300     # For report generation prompt

# UI Configuration
RESEARCH_DEPTH_OPTIONS = ["Overview", "Detailed", "Deep Dive"]
DEFAULT_ITERATIONS = 5
MAX_ITERATIONS = 10
MIN_ITERATIONS = 1

# Pagination
PAGE_SIZE = 10