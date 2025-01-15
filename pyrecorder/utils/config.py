import os
from dotenv import load_dotenv
load_dotenv()

TRANSCRIBE_FOLDER="docs/transcriptions"
CONVERSATIONS_FOLDER="docs/conversations"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

