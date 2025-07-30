import os
import time
import uuid
from playsound import playsound
import azure.cognitiveservices.speech as speechsdk
import google.generativeai as genai
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import queue

# --- 1. CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

# Configure API keys and settings
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Validate that all necessary environment variables are set
if not all([AZURE_SPEECH_KEY, AZURE_SPEECH_REGION, GEMINI_API_KEY, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID]):
    raise ValueError("One or more required environment variables are not set. Please check your .env file.")

# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)


class ConversationalAI:
    """
    Manages the conversational AI logic, separating it from the UI.
    """
    def __init__(self, update_queue):
        """
        Initializes the AI.
        :param update_queue: A queue.Queue object to send updates to the GUI.
        """
        self.chat_session = None
        self.is_running = False
        self.update_queue = update_queue

    def _send_update(self, msg_type, value):
        """Helper to send updates to the GUI thread."""
        self.update_queue.put({"type": msg_type, "value": value})

    def load_persona(self, file_path):
        """Loads the AI's persona from a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                persona = f.read()
            self._send_update("log", f"👤 Persona loaded from {os.path.basename(file_path)}.")
            return persona
        except FileNotFoundError:
            self._send_update("log", f"⚠️ Warning: Persona file '{file_path}' not found.")
            return "You are a helpful AI assistant."

    def start_session(self, persona_name):
        """Initializes a new chat session with a given persona."""
        self._send_update("status", "Initializing...")
        persona_file_path = os.path.join("personas", f"{persona_name}.txt")
        persona_prompt = self.load_persona(persona_file_path)

        model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat_session = model.start_chat(history=[
            {'role': 'user', 'parts': [persona_prompt]},
            {'role': 'model', 'parts': ["Understood. I will now respond as this persona."]}
        ])
        self.is_running = True
        self._send_update("status", f"Ready to chat as {persona_name}. Say something!")
        self._send_update("session_started", None)

    def stop_session(self):
        """Stops the current session."""
        if self.is_running:
            self.is_running = False
            self.chat_session = None
            self._send_update("status", "Session ended. Select a persona and start a new session.")
            self._send_update("session_stopped", None)
            self._send_update("log", "\n✅ Conversation ended.")

    def transcribe_from_microphone(self):
        """Captures a single utterance from the microphone."""
        if not self.is_running:
            return ""
            
        self._send_update("status", "Listening...")
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            self._send_update("log", f"🎙️ You: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            self._send_update("log", "❓ Understood nothing.")
            self._send_update("status", "Couldn't hear you. Try again.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            if self.is_running:
                self._send_update("log", f"🚫 Canceled: {result.cancellation_details.reason}")
                self._send_update("status", "Speech recognition canceled.")
        return ""

    def get_gemini_response(self, question):
        """Gets a contextual response from the Gemini chat session."""
        self._send_update("status", "🧠 Thinking...")
        try:
            response = self.chat_session.send_message(question)
            full_response = "".join(part.text for part in response.parts)
            self._send_update("log", f"🤖 Bot: {full_response}")
            return full_response
        except Exception as e:
            self._send_update("log", f"An error occurred with the Gemini API: {e}")
            return "Sorry, I'm having trouble thinking right now."

    # --- CORRECTED FUNCTION ---
    def speak_text_with_elevenlabs(self, text):
        """
        Generates audio, saves it to a temporary MP3 file, and plays it
        using the 'playsound' library to avoid audio driver conflicts.
        """
        if not text or not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID or not self.is_running:
            return

        self._send_update("status", "💬 Generating audio...")
        file_name = f"temp_audio_{uuid.uuid4()}.mp3"
        try:
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            
            # Generate audio as MP3 data using the correct method
            response_iterator = client.text_to_speech.convert(
                voice_id=ELEVENLABS_VOICE_ID,
                text=text,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )

            # Write the chunks from the iterator to the temporary file
            with open(file_name, "wb") as f:
                for chunk in response_iterator:
                    f.write(chunk)
            
            if not self.is_running:
                return # Session may have been stopped during generation

            # Play the audio file using playsound (this is a blocking call)
            self._send_update("status", "💬 Speaking...")
            playsound(file_name)
            
        except Exception as e:
            self._send_update("log", f"An error occurred during audio playback: {e}")
        finally:
            # Clean up the temporary file in all cases (success, error, etc.)
            if os.path.exists(file_name):
                os.remove(file_name)


    def run_conversation_loop(self):
        """Runs the main conversation loop, continuously listening."""
        while self.is_running:
            question_text = self.transcribe_from_microphone()

            if not self.is_running:
                break

            if not question_text:
                continue

            exit_phrases = ("goodbye", "exit", "stop", "that's all")
            if any(phrase in question_text.lower() for phrase in exit_phrases):
                self.speak_text_with_elevenlabs("Goodbye!")
                self.stop_session()
                break

            answer_text = self.get_gemini_response(question_text)
            self.speak_text_with_elevenlabs(answer_text)