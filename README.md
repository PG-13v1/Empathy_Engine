# The Empathy Engine 🎙️

An advanced AI service that converts text into emotionally expressive speech by detecting nuanced emotions and dynamically modulating vocal parameters based on both emotion type and intensity.

## Features

### Core Capabilities
✨ **Rich Emotion Detection**
- 6 distinct emotional states: joy, sadness, anger, surprise, inquisitive, concerned
- Dynamic intensity scaling (low, medium, high)
- Contextual analysis of text markers and punctuation

🗣️ **Sophisticated Voice Modulation**
- Dynamic adjustment of rate, pitch, and volume
- Intensity-based parameter scaling
- Support for both pyttsx3 (offline) and ElevenLabs (cloud) TTS

🔧 **Advanced Controls**
- Markdown-like SSML syntax support:
  - `**text**` for emphasis
  - `...` for pauses
  - `_text_` for slower speech
- Automatic intensity detection from text markers
- Fallback support for offline TTS

### Technical Features
- Flask-based web interface
- Command-line interface (CLI)
- Configurable voice profiles
- Easy integration with ElevenLabs API

## Setup
1. Clone and navigate to the repository:
    ```bash
    git clone https://github.com/PG-13v1/Empathy_Engine.git
    cd Empathy_Engine
    cd empathy_engine
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure ElevenLabs (optional):
   - Create `.env` file in project root
   - Add: `ELEVENLABS_API_KEY=your_api_key_here`

5. Run the application:
    ```bash
    python main.py         # Web interface
    python main.py --cli   # CLI mode
    ```

## Usage Examples

```python
# Basic usage
"This is a normal statement"  # Neutral tone

# With emphasis
"This is **really** important!"  # Emphasized speech

# With pauses
"Think about it... carefully"  # Includes pause

# High intensity
"This is absolutely amazing!!!"  # Elevated emotion

# Low intensity with slow speech
"I'm a bit _worried_ about this"  # Slower delivery
```

## Voice Parameter Mapping

Each emotion has three intensity levels affecting:
- Speech rate (130-200 words/min)
- Volume (0.6-1.0)
- Pitch (very_low to very_high)

Example mapping:
- Joy (high): faster rate, full volume, higher pitch
- Sadness (high): slower rate, reduced volume, lower pitch
- Anger (high): fastest rate, full volume, highest pitch

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
