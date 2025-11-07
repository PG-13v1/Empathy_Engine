# app/voice_engine.py

import os
import time
import pyttsx3
import requests
from dotenv import load_dotenv
from pathlib import Path
from . import config
import re
from typing import Tuple

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OUTPUT_DIR = Path("static/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Enhanced emotion mapping with intensity levels
EMOTION_SETTINGS = {
    "joy": {
        "low": {"rate": 170, "volume": 0.9, "pitch": "medium_high"},
        "medium": {"rate": 180, "volume": 1.0, "pitch": "high"},
        "high": {"rate": 190, "volume": 1.0, "pitch": "very_high"}
    },
    "sadness": {
        "low": {"rate": 150, "volume": 0.8, "pitch": "medium_low"},
        "medium": {"rate": 140, "volume": 0.7, "pitch": "low"},
        "high": {"rate": 130, "volume": 0.6, "pitch": "very_low"}
    },
    "anger": {
        "low": {"rate": 170, "volume": 0.9, "pitch": "medium_high"},
        "medium": {"rate": 190, "volume": 1.0, "pitch": "high"},
        "high": {"rate": 200, "volume": 1.0, "pitch": "very_high"}
    },
    "surprise": {
        "low": {"rate": 170, "volume": 0.9, "pitch": "high"},
        "medium": {"rate": 180, "volume": 1.0, "pitch": "very_high"},
        "high": {"rate": 190, "volume": 1.0, "pitch": "very_high"}
    },
    "inquisitive": {
        "low": {"rate": 160, "volume": 0.8, "pitch": "medium_high"},
        "medium": {"rate": 165, "volume": 0.9, "pitch": "high"},
        "high": {"rate": 170, "volume": 1.0, "pitch": "very_high"}
    },
    "concerned": {
        "low": {"rate": 155, "volume": 0.8, "pitch": "medium_low"},
        "medium": {"rate": 150, "volume": 0.9, "pitch": "low"},
        "high": {"rate": 145, "volume": 1.0, "pitch": "very_low"}
    }
}

def process_ssml(text: str) -> str:
    """Convert simple markdown-like syntax to SSML"""
    ssml = f"""<?xml version="1.0"?>
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">
    """
    
    # Convert **text** to emphasized text
    text = re.sub(r'\*\*(.*?)\*\*', r'<emphasis>\1</emphasis>', text)
    
    # Convert ... to pauses
    text = re.sub(r'\.{3}', '<break time="1s"/>', text)
    
    # Convert _text_ to reduced rate
    text = re.sub(r'_(.*?)_', r'<prosody rate="slow">\1</prosody>', text)
    
    ssml += text + "</speak>"
    return ssml

def determine_intensity(text: str, base_emotion: str) -> Tuple[str, str]:
    """Determine emotion intensity based on text analysis"""
    # Check for intensity indicators
    intensity_markers = {
        "high": ["!", "extremely", "very", "super", "absolutely", "completely"],
        "medium": ["quite", "rather", "pretty", "somewhat"],
        "low": ["slightly", "a bit", "kind of", "sort of"]
    }
    
    text_lower = text.lower()
    exclamation_count = text.count('!')
    
    # Check for intensity markers
    for intensity, markers in intensity_markers.items():
        if any(marker in text_lower for marker in markers):
            return base_emotion, intensity
            
    # Default intensity based on punctuation
    if exclamation_count >= 2:
        return base_emotion, "high"
    elif exclamation_count == 1:
        return base_emotion, "medium"
    return base_emotion, "low"

def _text_to_speech_pyttsx3(text: str, emotion: str, intensity: str, filename: str):
    engine = pyttsx3.init()
    
    # Get settings based on emotion and intensity
    settings = EMOTION_SETTINGS[emotion][intensity]
    
    engine.setProperty('rate', settings['rate'])
    engine.setProperty('volume', settings['volume'])
    
    # Map pitch settings to voices
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        if settings['pitch'] in ['very_high', 'high']:
            engine.setProperty('voice', voices[1].id)
        elif settings['pitch'] in ['very_low', 'low']:
            engine.setProperty('voice', voices[0].id)
    
    # Process any SSML-like markup
    processed_text = process_ssml(text)
    
    full_path = OUTPUT_DIR / filename
    engine.save_to_file(processed_text, str(full_path))
    engine.runAndWait()
    return str(full_path)

def _text_to_speech_elevenlabs(text: str, emotion: str, intensity: str, filename: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"
    
    # Map emotion and intensity to ElevenLabs parameters
    settings = EMOTION_SETTINGS[emotion][intensity]
    
    stability = 0.75 - (0.1 * ["low", "medium", "high"].index(intensity))
    similarity_boost = 0.6 + (0.1 * ["low", "medium", "high"].index(intensity))
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # Include SSML processing
    processed_text = process_ssml(text)
    
    data = {
        "text": processed_text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        full_path = OUTPUT_DIR / filename
        with open(full_path, "wb") as f:
            f.write(response.content)
        return str(full_path)
    else:
        raise Exception(f"ElevenLabs error: {response.status_code} - {response.text}")

def generate_speech(text: str, emotion: str) -> str:
    # Determine emotion intensity
    emotion, intensity = determine_intensity(text, emotion)
    
    timestamp = str(int(time.time()))
    filename = f"output_{emotion}_{intensity}_{timestamp}.{'mp3' if ELEVENLABS_API_KEY else 'wav'}"

    if ELEVENLABS_API_KEY:
        return _text_to_speech_elevenlabs(text, emotion, intensity, filename)
    else:
        return _text_to_speech_pyttsx3(text, emotion, intensity, filename)