import openai
from pyrecorder.utils.config import OPENAI_API_KEY
import time
import whisper

class OpenAI:
    """
    A class to interact with OpenAI's GPT API.
    """

    def __init__(self, api_key=None, model="gpt-4", retries=3):
        """
        Initialize the OpenAI client.

        :param api_key: The OpenAI API key. If None, it uses the key from the config.
        :param model: The default model to use for API calls.
        :param retries: The number of retries in case of rate-limiting or errors.
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model
        self.retries = retries
        self.whisper_model = whisper.load_model("base")


        # Set the OpenAI API key
        openai.api_key = self.api_key
        
        self.client = openai.OpenAI(api_key=str(self.api_key))

    
    def whisper_transcribe(self, audio_np, fp16=False):
        try:
            print("Transcribing audio...")
            transcribed_text = self.whisper_model.transcribe(audio_np, fp16=False)["text"]
            print("Transcription complete.")

            return transcribed_text

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return # Stop retrying on unknown errors


    def send_prompt(self, prompt, system_message="You are a helpful assistant."):
        """
        Send a prompt to the OpenAI API and get a response.

        :param prompt: The user input or query.
        :param system_message: An optional system message for context setting.
        :return: The response from OpenAI or None in case of failure.
        """
        for attempt in range(self.retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},
                    ],
                )
                # Return the assistant's response content
                return response.choices[0].message.content

            except openai.RateLimitError:
                print(f"Rate limit exceeded. Retrying in {5} seconds...")
                time.sleep(5)  # Wait before retrying

            except openai.BadRequestError as e:
                print(f"Invalid request: {e}")
                break  # No point in retrying if the request is invalid

            except openai.OpenAIError as e:
                print(f"An OpenAI error occurred: {e}")
                time.sleep(2)  # Wait briefly before retrying

            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break  # Stop retrying on unknown errors

        return None

    def get_organized_conversation(self, transcription_text):
        """
        Organize and extract key information from a conversation transcription.

        :param transcription_text: The raw transcription text.
        :return: The organized response from ChatGPT.
        """
        prompt = (
            f"Hello GPT, this is an interaction via phone in a restaurant. "
            f"It is between a seller and a customer. Organize and take out important information:\n{transcription_text}"
        )
        return self.send_prompt(prompt)

    def get_labeled_conversation(self, transcription_text):
        """
        Add labels to a conversation transcription.

        :param transcription_text: The raw transcription text.
        :return: The labeled response from ChatGPT.
        """
        prompt = f"Present the conversation with labels:\n{transcription_text}"
        return self.send_prompt(prompt)
