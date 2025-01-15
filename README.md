# AI-Powered Audio Transcription and Conversation Processing

This project is an AI-driven system for recording audio, transcribing it using OpenAI's Whisper, and organizing the conversation using OpenAI's GPT API. The application is ideal for scenarios like customer service calls, restaurant interactions, or any conversational context.

---

## Features

- **Real-time Audio Recording**:

  - Record audio indefinitely or for a specified duration.
  - Support for selecting specific audio input devices.

- **Speech-to-Text Transcription**:

  - Utilize OpenAI's Whisper model for accurate transcription of recorded audio.

- **AI-Powered Conversation Processing**:

  - Organize and extract key details from conversations.
  - Label conversation participants and structure interactions meaningfully.

- **Error Handling and Reliability**:
  - Automatic retries for rate-limiting or network errors.
  - Clear error messages for troubleshooting.

---

## Requirements

- Python 3.8 or higher
- OpenAI API Key
- Audio input device (e.g., microphone or virtual audio cable)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/brunoastr0/pyrecorder.git
   cd pyrecorder
   ```
