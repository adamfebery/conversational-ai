# Conversational AI (Powered by Gemini, ElevenLabs & More)

![Project Banner](https://placehold.co/800x250/1e293b/ffffff?text=AI%20Voice%20Bot&font=lato)

**A conversational AI that listens to your voice and responds in a custom-cloned voice, complete with swappable personalities.**

This project is a practical demonstration built as a follow-up to a webinar. It showcases how to integrate several powerful AI services to create a seamless, voice-driven conversational experience with dynamic personas.

No technical support is offered with this code, by running the demonstration you are verifying you are happy with the requirements listed in requirements.txt. Please verify all packages on your own. We do not recommend running this application in a production environment.

---

## ✨ Features

- 🎙️ **Real-time Voice Input**: Actively listens for user questions via the microphone.  
- ✍️ **High-Accuracy Transcription**: Utilizes **Azure Cognitive Services** for precise speech-to-text conversion.  
- 🧠 **Intelligent Response Generation**: Leverages the **Google Gemini API** to provide context-aware and coherent answers.  
- 🗣️ **Custom Voice Output**: Converts text responses back into speech using a unique, cloned voice from **ElevenLabs**.  
- 🎭 **Dynamic Personas**: Easily load different personalities for the bot from simple text files at runtime.  

---

## ⚙️ How It Works

The application initializes by loading a persona, then enters a loop to process voice commands and generate a spoken response.

```mermaid
    A -->[Start Application] --> B{Load Persona File};
    B --> C[🎙️ User Speaks];
    C -->|Microphone Input| D(Azure Speech-to-Text);
    D -->|Transcribed Text| E{Google Gemini API};
    E -->|Generated Answer| F(ElevenLabs Text-to-Speech);
    F -->|Audio Stream| G[🔊 Bot Responds];
    G --> End the conversation by saying "Goodbye."
```

## 📂 Project Structure

The application automatically creates the following directories. Organize your files as shown below for full functionality:

* `assets/` - Contains static audio files used by the application.
    * Optional - create if you want to use local audio rather than generate via the LLM.
* `personas/` - Holds `.txt` files that define the AI's personality and instructions.
    * `anna-helpdesk-lostpass.txt`
* `scripts/` - Stores timed `.txt` script files that correspond with demonstrations.
    * Optional - create if you want to use a script eather than rely on LLM.
* `.env` - Stores your secret API keys and region information. This file is ignored by Git.
* `.gitignore` - Specifies files and directories that Git should ignore.
* `gui.py` - The main application file that runs the graphical user interface.
* `persona_refactored.py` - The core Python class that handles all AI logic, including transcription, response generation, and text-to-speech.
* `requirements.txt` - A list of the Python dependencies needed to run the project.

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | Core Application Logic |
| ![Tkinter](https://img.shields.io/badge/Tkinter-2B5B84?style=for-the-badge&logo=python&logoColor=white) | Graphical User Interface |
| ![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white) | Speech-to-Text |
| ![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white) | AI Language Model |
| ![ElevenLabs](https://img.shields.io/badge/ElevenLabs-1A1A1A?style=for-the-badge&logo=elevenlabs&logoColor=white) | Custom Voice Synthesis |
| ![VLC](https://img.shields.io/badge/VLC-FF8800?style=for-the-badge&logo=vlcmediaplayer&logoColor=white) | Video & Audio Playback |

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

***

### Prerequisites

Before you begin, ensure you have the following:

* **Python 3.8 or newer** installed.
* **Git** installed to clone the repository.
* **VLC Media Player**: The application uses the VLC engine for video and audio playback. Please [install VLC](https://www.videolan.org/vlc/) on your system.
* **API Keys** for:
    * Azure Cognitive Services
    * Google AI Studio (for the Gemini API)
    * ElevenLabs (including a Voice ID for your cloned voice)

***

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/adamfebery/conversational-ai.git](https://github.com/adamfebery/conversational-ai.git)
    cd conversational-ai
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    *(Note: Please ensure your `requirements.txt` is up-to-date. It should include `sounddevice` for audio output and `python-vlc` for media playback.)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment variables:**
    Create a file named `.env` in the project root. Copy the structure below and add your secret API keys and configuration details.
    ```dotenv
    # Azure Cognitive Services
    AZURE_SPEECH_KEY=YOUR_AZURE_API_KEY
    AZURE_SPEECH_REGION=YOUR_AZURE_REGION

    # Google Gemini
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY

    # ElevenLabs
    ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
    ELEVENLABS_VOICE_ID=YOUR_CLONED_VOICE_ID
    ```

5.  **Add your persona files:**
    Create `.txt` files in the `personas` directory for each persona you want. For example, `personas/bob.txt`:
    ```txt
    You are Bob, a friendly and slightly sarcastic assistant from Liverpool. You love talking about football and the weather. Keep your answers brief and witty.
    ```

***

### Running the Application

1.  **Run the `gui.py` script from your terminal:**
    ```bash
    python gui.py
    ```

2.  **Using the App:**
    The application will start. Select a persona from the list and click "Start Session" to begin the live conversation.

    ## ⚖️ License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or want to fix a bug, please feel free to:

1.  Fork the repository.
2.  Create a new branch
3.  Commit your changes
4.  Push to the branch 
5.  Open a Pull Request.

