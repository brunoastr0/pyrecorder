import os
from dotenv import load_dotenv
load_dotenv()

TRANSCRIBE_FOLDER="docs/transcriptions"
CONVERSATIONS_FOLDER="docs/conversations"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
DEVICE_NAME=os.getenv("DEVICE_NAME")
SAMPLE_RATE=os.getenv("SAMPLE_RATE")

