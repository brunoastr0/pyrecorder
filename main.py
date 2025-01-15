
import numpy as np
from pyrecorder.AudioRecorder.AudioRecorder import AudioRecorder
from pyrecorder.OpenAI.OpenAI import OpenAI
from pyrecorder.utils.config import OPENAI_API_KEY
from pyrecorder.utils.config import CONVERSATIONS_FOLDER
from pyrecorder.utils.config import TRANSCRIBE_FOLDER
from pyrecorder.utils.config import DEVICE_NAME
from pyrecorder.utils.config import SAMPLE_RATE



from datetime import datetime




def save_to_file(content, filename):
    """
    Save content to a file.
    """
    filename = filename+".txt"
    with open(filename, "w") as file:
        file.write(content + "\n")


def main():
    """
    Main function to record, transcribe, and process audio.
    """
    # Initialize the AudioRecorder
    try:
        recorder = AudioRecorder(device_name=DEVICE_NAME, sample_rate=SAMPLE_RATE)
        print(f"Using device '{DEVICE_NAME}' (index {recorder.device_index})")
    except ValueError as e:
        print(e)
        return

    try:
        # Initialize OpenAI client
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        # Record audio indefinitely until stopped
        audio_data = recorder.record_audio_indefinitely()

        if audio_data is None or len(audio_data) == 0:
            print("No audio recorded. Exiting...")
            return

        audio_np = np.array(audio_data, dtype=np.float32).squeeze()  # Ensure 1D array

        transcription = openai_client.whisper_transcribe(audio_np)

        # Get responses from ChatGPT
        print("Fetching responses from ChatGPT...")
        organized_conversations = openai_client.get_organized_conversation(transcription)
        labeled_conversations = openai_client.get_labeled_conversation(transcription)

        # Save responses
        if organized_conversations:
            save_to_file(organized_conversations, TRANSCRIBE_FOLDER+"/transcriptions"+str(datetime.now()))
        if labeled_conversations:
            save_to_file(labeled_conversations, CONVERSATIONS_FOLDER+"/conversations"+str(datetime.now()))

    except KeyboardInterrupt:
        print("\nRecording stopped manually.")

    finally:
        print("Process complete. Transcription and responses saved.")

if __name__ == "__main__":
    main()
