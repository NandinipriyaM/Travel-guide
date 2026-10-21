# 🌍 AI-Powered Travel Guide using Gemini AI & Murf.AI

An AI-powered web application that generates informative descriptions of tourist destinations and converts them into natural-sounding audio guides using Generative AI and text-to-speech technology.

## 🚀 Live Demo

**Live Application:** https://travel-guide-1-39nq.onrender.com/

## 📌 About the Project

The AI-Powered Travel Guide helps users explore tourist destinations without depending entirely on traditional tour guides or lengthy articles.

Users can enter a destination, select their preferred language and description length, and generate an AI-powered travel guide with both text and audio output.

## ✨ Key Features

- 🤖 **AI-Generated Descriptions:** Uses Google Gemini AI to generate information about tourist destinations.
- 🔊 **Text-to-Speech:** Uses Murf.AI to convert generated descriptions into audio.
- 🌐 **Multilingual Support:** Supports English, Hindi, Tamil, and Telugu.
- 📝 **Flexible Guide Length:** Choose summary or detailed descriptions.
- 🎙️ **Voice Selection:** Supports available male and female voice options.
- 🎧 **Audio Playback:** Listen to generated travel guides.
- 📖 **Text Output:** Read the generated description alongside the audio.
- 💻 **Web-Based Interface:** Access the application through a browser.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Backend API |
| HTML | Web page structure |
| JavaScript | Frontend interactions and API requests |
| Google Gemini API | Travel description generation |
| Murf.AI API | AI speech generation |
| Flask-CORS | Cross-origin API communication |

## 🏗️ Project Architecture

```text
User
  |
  v
Frontend (HTML + JavaScript)
  |
  v
Backend (Python + Flask)
  |
  +--------------------+
  |                    |
  v                    v
Google Gemini API    Murf.AI API
  |                    |
  v                    v
Travel Description   Audio Generation
  |                    |
  +---------+----------+
            |
            v
    Text and Audio Output
```

## 📂 Project Structure

```text
travel-guide/
├── Backend/
│   ├── app.py
│   └── requirements.txt
└── Frontend/
    ├── index.html
    └── index.js
```

### Folder Details

**Backend/**
- `app.py` — Flask server, API endpoints, AI-generated descriptions, and audio generation logic.
- `requirements.txt` — Python dependencies required to run the backend.

**Frontend/**
- `index.html` — User interface for selecting destinations and guide preferences.
- `index.js` — Handles user interactions, sends requests to the backend, and displays generated text and audio.

## ⚙️ How It Works

1. The user enters a tourist destination.
2. The user selects the preferred language, guide length, and available voice options.
3. The frontend sends the selected options to the Flask backend.
4. Google Gemini AI generates the travel description.
5. Murf.AI converts the generated description into speech.
6. The application displays the description and provides audio playback.

## 💻 Run Locally

### Prerequisites

- Python installed on your system.
- A Google Gemini API key.
- A Murf.AI API key.
- Git installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/NandinipriyaM/Travel-guide.git
cd Travel-guide
```

### 2. Install Backend Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 3. Configure API Keys

Set your API keys as environment variables, using the variable names expected by `Backend/app.py`.

For example, on Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:MURF_API_KEY="your_murf_api_key"
```

On macOS or Linux:

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export MURF_API_KEY="your_murf_api_key"
```

### 4. Start the Backend

From the `Backend` directory, run:

```bash
python app.py
```

Use the local server address printed in your terminal.



**Build. Connect. Learn. Grow.**
