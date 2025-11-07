EMOTION_VOICE_MAP = {
    "joy": {"rate": 200, "pitch": "high", "volume": 1.0},
    "surprise": {"rate": 180, "pitch": "high", "volume": 0.9},
    "neutral": {"rate": 150, "pitch": "medium", "volume": 0.8},
    "sadness": {"rate": 120, "pitch": "low", "volume": 0.7},
    "anger": {"rate": 170, "pitch": "low", "volume": 0.95},
    "fear": {"rate": 140, "pitch": "medium", "volume": 0.75},
    "disgust": {"rate": 130, "pitch": "low", "volume": 0.7},
}

# Fallback for unknown emotions
DEFAULT_VOICE_SETTINGS = EMOTION_VOICE_MAP["neutral"]

# ElevenLabs settings
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"