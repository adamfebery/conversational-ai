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

# Validate that all necessary environment variables are set
if not all([azure_speech_key, azure_speech_region, gemini_api_key, elevenlabs_api_key, elevenlabs_voice_id]):
    raise ValueError("One or more required environment variables are not set. Please check your .env file.")


# --- 2. FUNCTION DEFINITIONS ---

def load_persona(file_path=".persona-aw"):
    """Loads the AI's persona from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            persona = f.read()
            print(f"👤 Persona loaded from {file_path}.")
            return persona
    except FileNotFoundError:
        print(f"⚠️  Warning: Persona file '{file_path}' not found. The AI will respond without a specific persona.")
        # Return a neutral, empty persona if the file doesn't exist
        return "You are a helpful AI assistant."

def transcribe_from_microphone():
    """Captures audio from the microphone and transcribes it to text using Azure Speech Service."""
    print("Listening for your question...")
    # TODO: We will implement this function in the next step.
    transcribed_text = "What is the distance between Earth and the Moon?" # Placeholder text
    print(f"🎙️ You said: {transcribed_text}")
    return transcribed_text

def get_gemini_response(question, persona):
    """Sends the question and persona to Gemini and returns the text response."""
    print("🧠 Thinking (with persona)...")
    # TODO: We will implement this function later.
    # The 'persona' will be prepended to the user's question to guide the model's response style.
    # Placeholder response that reflects a persona
    answer = "Ah, a question about the heavens! As a wise, old astronomer, I can tell you that the Moon, our lovely celestial neighbor, keeps an average distance of about 384,400 kilometers from our home, the Earth."
    print(f"🤖 Gemini's Persona Answer: {answer}")
    return answer

def speak_text_with_elevenlabs(text):
    """Converts text to speech using ElevenLabs and plays it."""
    print("💬 Speaking...")
    # TODO: We will implement this function later.
    # This function will call the ElevenLabs API and stream the audio.
    pass


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    # Load the persona from the specified file
    persona_prompt = load_persona(".persona-aw")

    # Step 1: Get the user's question from their voice
    question_text = transcribe_from_microphone()

    # Step 2: Get an answer from Gemini, guided by the persona
    answer_text = get_gemini_response(question_text, persona_prompt)

    # Step 3: Speak the answer using the cloned voice
    speak_text_with_elevenlabs(answer_text)

    print("\n✅ Script finished.")