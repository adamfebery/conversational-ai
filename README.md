
> # AI Voice Bot Project
> 
> Welcome! This repository contains the source code for the AI Voice Bot we're building together. This project is a practical follow-up to my webinar, demonstrating how to connect several powerful AI services to create a conversational assistant that responds in a custom-cloned voice.
> 
> ## Features
> 
> -   🎙️ **Voice Input**: Listens for a user's question via their microphone.
>     
> -   ✍️ **Speech-to-Text**: Uses **Azure Cognitive Services** to transcribe spoken language into text.
>     
> -   🧠 **Intelligent Answers**: Leverages the **Google Gemini API** to generate relevant and coherent answers.
>     
> -   🗣️ **Cloned Voice Output**: Converts the text answer back into speech using a custom voice from **ElevenLabs**.
>     
> 
> ----------
> 
> ## Tech Stack
> 
> This project is built with Python and integrates the following services:
> 
> -   **Python 3**
>     
> -   **Azure Cognitive Services for Speech**
>     
> -   **Google Gemini API**
>     
> -   **ElevenLabs API**
>     
> 
> ----------
> 
> ## Getting Started
> 
> Follow these steps to get the project running on your local machine.
> 
> ### Prerequisites
> 
> 1.  **Python**: Ensure you have Python 3.8 or newer installed.
>     
> 2.  **API Keys**: You'll need accounts and API keys for:
>     
>     -   Azure Cognitive Services
>         
>     -   Google AI Studio (for the Gemini API key)
>         
>     -   ElevenLabs (including a Voice ID for your cloned voice)
>         
> 3.  **Git**: You need Git installed to clone this repository.
>     
> 
> ### Installation & Setup
> 
> 1.  **Clone the repository:**
>     
>     Bash
>     
>     ```
>     git clone <your-repo-url>
>     cd <your-repo-name>
>     
>     ```
>     
> 2.  **Create the environment file:** Create a file named `.env` in the project root. Copy the contents below into it and add your secret API keys and region information.
>     
>     _.env file structure:_
>     
>     Code snippet
>     
>     ```
>     # Azure Cognitive Services
>     AZURE_SPEECH_KEY=YOUR_AZURE_API_KEY
>     AZURE_SPEECH_REGION=YOUR_AZURE_REGION
>     
>     ```
>     

> ```
> # Google Gemini
> GEMINI_API_KEY=YOUR_GEMINI_API_KEY
> 
> ```

> ```
> # ElevenLabs
> ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
> ELEVENLABS_VOICE_ID=YOUR_CLONED_VOICE_ID
> ```
> 
> ```
> 
> 3.  **Install dependencies:** Install all the necessary Python packages using the `requirements.txt` file.
>     
>     Bash
>     
>     ```
>     pip install -r requirements.txt
>     
>     ```
>     
> 
> ### Running the Application
> 
> Once everything is installed and configured, run the main script from your terminal:
> 
> Bash
> 
> ```
> python main.py
> 
> ```
> 
> The script will then listen for your voice, process your question, and respond out loud.