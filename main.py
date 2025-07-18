import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

# Configure API keys and settings
azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
gemini_api_key = os.getenv("GEMINI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")


# --- 2. FUNCTION DEFINITIONS ---

def transcribe_from_microphone():
    """Captures audio from the microphone and transcribes it to text using Azure Speech Service."""
    print("Listening for your question...")
    # TODO: We will implement this function in the next step.
    transcribed_text = "What is the distance between Earth and the Moon?" # Placeholder text
    print(f"🎙️ You said: {transcribed_text}")
    return transcribed_text

def get_gemini_response(question):
    """Sends the question to Gemini and returns the text response."""
    print("🧠 Thinking...")
    # TODO: We will implement this function later.
    answer = "The average distance between Earth and the Moon is about 384,400 kilometers." # Placeholder text
    print(f"🤖 Gemini's Answer: {answer}")
    return answer

def speak_text_with_elevenlabs(text):
    """Converts text to speech using ElevenLabs and plays it."""
    print("💬 Speaking...")
    # TODO: We will implement this function later.
    # This function will call the ElevenLabs API and stream the audio.
    pass


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    # Step 1: Get the user's question from their voice
    question_text = transcribe_from_microphone()

    # Step 2: Get an answer from Gemini
    answer_text = get_gemini_response(question_text)

    # Step 3: Speak the answer using the cloned voice
    speak_text_with_elevenlabs(answer_text)

    print("\n✅ Script finished.")