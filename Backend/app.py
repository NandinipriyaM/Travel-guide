
import os
import base64
import tempfile
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

# Load API keys from backend/.env
load_dotenv(
    os.path.join(os.path.dirname(__file__), ".env")
)

app = Flask(__name__)
CORS(app)

# Read API keys from environment variables
MURF_API_KEY = os.getenv("MURF_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not MURF_API_KEY or not GEMINI_API_KEY:
    raise RuntimeError(
        "Missing API keys. Configure MURF_API_KEY and "
        "GEMINI_API_KEY in your .env file or deployment settings."
    )

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


PROMPTS = {
    "Summary": """
You are a professional tourist guide.
Provide a high-level overview of "{place}" in {language}.

Focus on:
- The historical significance
- Why the place is famous
- Key architectural or cultural highlights

Keep the explanation concise, engaging, and easy to follow.
Avoid excessive details and dates.
Limit the response to around 200 words.

Respond ONLY in {language}.
""",

    "Detailed": """
You are a professional tourist guide.
Provide a detailed and immersive explanation of "{place}" in {language}.

Cover:
- Historical background and timeline
- Architectural design and unique features
- Cultural importance and notable events
- Interesting facts and visitor insights

Explain concepts clearly and in a storytelling manner.
Include relevant details and examples to create a rich experience.
Limit the response to around 400 words.

Respond ONLY in {language}.
"""
}


def generate_speech(text, voice_id, locale):
    url = "https://global.api.murf.ai/v1/speech/stream"

    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "voice_id": voice_id,
        "text": text,
        "locale": locale,
        "model": "FALCON",
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "MONO"
    }

    # Request audio from Murf
    response = requests.post(
        url,
        headers=headers,
        json=data,
        stream=True,
        timeout=120
    )

    response.raise_for_status()

    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )
    audio_path = temp_audio.name
    temp_audio.close()

    try:
        with open(audio_path, "wb") as audio_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    audio_file.write(chunk)

        return audio_path

    except Exception:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise

    finally:
        response.close()


def generate_description(place, answer_type, language):
    if answer_type not in PROMPTS:
        raise ValueError(
            "answerType must be 'Summary' or 'Detailed'."
        )

    prompt = PROMPTS[answer_type].format(
        place=place,
        language=language
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text


@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    audio_path = None

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "A valid JSON request body is required."
            }), 400

        required_fields = [
            "place",
            "answerType",
            "language",
            "voiceId",
            "locale"
        ]

        missing_fields = [
            field for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields.",
                "fields": missing_fields
            }), 400

        place = data["place"]
        answer_type = data["answerType"]
        language = data["language"]
        voice_id = data["voiceId"]
        locale = data["locale"]

        # Step 1: Generate the description with Gemini
        text_description = generate_description(
            place,
            answer_type,
            language
        )

        # Step 2: Generate speech with Murf
        audio_path = generate_speech(
            text_description,
            voice_id,
            locale
        )

        # Step 3: Encode the MP3 audio as Base64
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        encoded_audio = base64.b64encode(
            audio_bytes
        ).decode("utf-8")

        # Step 4: Return the same response fields to the frontend
        return jsonify({
            "description": text_description,
            "audioBase64": encoded_audio
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except requests.RequestException:
        app.logger.exception("Murf API request failed.")
        return jsonify({
            "error": "Audio generation failed. Please try again."
        }), 502

    except Exception:
        app.logger.exception("Audio guide generation failed.")
        return jsonify({
            "error": "Failed to generate the audio guide."
        }), 500

    finally:
        # Delete the temporary audio file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    app.run(debug=True)
