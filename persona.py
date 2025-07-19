import os
import azure.cognitiveservices.speech as speechsdk
import google.generativeai as genai
import argparse
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import pyaudio

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

# Configure APIs
genai.configure(api_key=gemini_api_key)


# --- 2. FUNCTION DEFINITIONS ---

def load_persona(file_path):
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
    """Captures a single utterance from the microphone."""
    print("Listening...")
    speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key, region=azure_speech_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"🎙️ You: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❓ Understood nothing.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print(f"🚫 Canceled: {result.cancellation_details.reason}")
    return ""

def get_gemini_response(chat_session, question):
    """Gets a contextual response from the Gemini chat session."""
    print("🧠 Thinking (with persona)...")
    try:
        response = chat_session.send_message(question)
        full_response = "".join(part.text for part in response.parts)
        print(f"🤖 Bot: {full_response}")
        return full_response
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I'm having trouble thinking right now."

def speak_text_with_elevenlabs(text):
    """Converts text to speech and plays it using PyAudio."""
    if not text or not elevenlabs_api_key or not elevenlabs_voice_id:
        return
        
    print("💬 Speaking...")
    try:
        client = ElevenLabs(api_key=elevenlabs_api_key)
        audio_stream = client.text_to_speech.stream(
            elevenlabs_voice_id, text=text, model_id="eleven_multilingual_v2", output_format="pcm_24000"
        )
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        for chunk in audio_stream:
            if chunk:
                stream.write(chunk)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
            
    except Exception as e:
        print(f"An error occurred during audio playback: {e}")


# --- 3. MAIN CONVERSATIONAL LOOP ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a conversational AI with a specific persona.")
    parser.add_argument(
        "--persona",
        required=True,
        help="The name of the persona to use from the 'personas' directory (e.g., 'bob' for 'personas/bob.txt')"
    )
    args = parser.parse_args()

    # Construct the persona file path from the command-line argument
    persona_file_path = os.path.join("personas", f"{args.persona}.txt")

    # Load the persona and initialize the Gemini Model with it
    persona_prompt = load_persona(persona_file_path)
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat = model.start_chat(history=[
        {'role': 'user', 'parts': [persona_prompt]},
        {'role': 'model', 'parts': ["Understood. I will now respond as this persona."]}
    ])
    
    exit_phrases = ("goodbye", "exit", "stop", "that's all")
    print(f"👋 Hello! I'm ready to chat with my persona. Say 'goodbye' to end.")
    
    while True:
        question_text = transcribe_from_microphone()
        if not question_text:
            continue

        if any(phrase in question_text.lower() for phrase in exit_phrases):
            speak_text_with_elevenlabs("Goodbye!")
            break

        answer_text = get_gemini_response(chat, question_text)
        speak_text_with_elevenlabs(answer_text)

    print("\n✅ Conversation ended.")