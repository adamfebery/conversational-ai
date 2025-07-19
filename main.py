import os
import azure.cognitiveservices.speech as speechsdk
import google.generativeai as genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import pyaudio

# --- 1. CONFIGURATION ---
load_dotenv()

azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
gemini_api_key = os.getenv("GEMINI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")

# Configure APIs
genai.configure(api_key=gemini_api_key)


# --- 2. FUNCTION DEFINITIONS ---

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
    print("🧠 Thinking...")
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
    # Initialize the Gemini Model and start a chat session
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat = model.start_chat(history=[])
    
    # A tuple of phrases that will end the conversation
    exit_phrases = ("goodbye", "exit", "stop", "that's all")
    
    print("👋 Hello! I'm ready to chat. Say 'goodbye' to end the conversation.")
    
    while True:
        # Get user's question
        question_text = transcribe_from_microphone()

        # If there's no input, just listen again
        if not question_text:
            continue

        # Check if any exit phrase is present in the user's speech
        user_input_lower = question_text.lower()
        if any(phrase in user_input_lower for phrase in exit_phrases):
            speak_text_with_elevenlabs("Goodbye!")
            break

        # Get and speak the bot's answer
        answer_text = get_gemini_response(chat, question_text)
        speak_text_with_elevenlabs(answer_text)

    print("\n✅ Conversation ended.")