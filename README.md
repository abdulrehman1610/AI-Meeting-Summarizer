# 📹 AI Meeting Summarizer

An intelligent, local-first web application built with Streamlit that automatically transcribes meeting recordings, generates concise summaries, extracts actionable tasks, and emails the results to your team.

## ✨ Features

- **Multi-Format Support**: Upload `.mp4`, `.mov`, `.m4a`, `.mp3`, `.wav`, or `.webm` files.
- **High-Quality Transcription**: Powered by OpenAI's Whisper models (choose between tiny, base, small, or medium).
- **Intelligent Summarization**: Uses advanced Large Language Models (via Ollama or OpenRouter) to distill meetings into key insights and structured action items.
- **Export & Share**:
  - Download comprehensive Markdown (`.md`) reports.
  - Automatically email summaries and action items to team members directly from the app.
- **Privacy-Focused**: Can be run entirely locally using Ollama and local Whisper models to ensure sensitive meeting data never leaves your machine.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) (Required for audio processing)
- [Ollama](https://ollama.com/) (Optional: If running LLMs locally)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdulrehman1610/AI-Meeting-Summarizer.git
   cd AI-Meeting-Summarizer
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add the following configuration:
   ```env
   LLM_BACKEND=openrouter  # or 'ollama'
   OLLAMA_MODEL=llama3
   OPENROUTER_API_KEY=your_openrouter_api_key
   
   # Required for the Email Module
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```
   *(Note: If using Gmail, you must use an [App Password](https://support.google.com/accounts/answer/185833).)*

### Running the App

Start the Streamlit application:
```bash
streamlit run app.py
```
Then navigate to `http://localhost:8501` in your browser.

## 📂 Project Structure

- `app.py`: Main Streamlit application UI.
- `modules/`
  - `ingest.py`: Handles file uploads, audio extraction, and chunking via FFmpeg/Pydub.
  - `transcriber.py`: Manages Whisper models and generates transcriptions.
  - `llm_processor.py`: Interfaces with Ollama and OpenRouter APIs for summarization.
  - `exporter.py`: Formats the parsed data into downloadable Markdown files.
  - `email_dispatcher.py`: Handles SMTP connections to send action items via email.
- `temp_chunks/`: Temporary directory for processing audio segments.
- `outputs/`: Generated markdown summaries.
- `sample_audio/`: Place test audio/video files here.

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - Web framework
- [Whisper](https://github.com/openai/whisper) - Speech recognition
- [OpenRouter](https://openrouter.ai/) / [Ollama](https://ollama.com/) - LLM Inference
- [Pydub](https://github.com/jiaaro/pydub) - Audio processing

## 📝 License

This project is open-source and available under the MIT License.
