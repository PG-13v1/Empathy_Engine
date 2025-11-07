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
    cd empathy-engine
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

## Design Choices
The design prioritizes clear separation between emotion detection, intensity scaling, and voice parameterization so each stage can be tested and tuned independently. Emotion detection uses a lightweight rule-and-feature approach (text markers, punctuation, token-level sentiment cues) combined with simple context windows rather than an opaque monolithic model; this eases debugging and lets downstream parameter mapping remain deterministic and predictable.

Mapping from emotion → voice parameters is explicit and parametric: each emotion defines a baseline triplet (rate, volume, pitch) and three intensity multipliers (low, medium, high). Rate is expressed in words-per-minute bounds, volume as a scalar 0.0–1.0, and pitch as an ordinal scale (very_low ... very_high) that the TTS backend translates to its native pitch values. Intensity adjusts these baselines multiplicatively for rate/volume and via discrete steps for pitch, which keeps changes perceptible without producing unnatural extremes.

Text markers and punctuation drive intensity heuristics: repeated punctuation (!!!, ???), capitalization, emphatic markers (bold) and ellipses ("...") increment internal intensity counters or toggle specific modulation behaviors (pauses for "...", slowed delivery for underscores, emphasis for bold). These markers are parsed before emotion-to-parameter mapping so the system can combine semantic emotion inference with explicit user cues to determine final intensity and SSML-like tags.

Backend abstraction and fallbacks were chosen to preserve behaviour across environments. A small translation layer converts the internal (rate, volume, pitch, pause) model into pyttsx3 commands for offline use or to ElevenLabs API parameters when available. Fallback rules clamp parameters to safe bounds when a backend does not support a given feature (e.g., approximate pitch via rate/volume adjustments), ensuring graceful degradation rather than failure.

Voicing profiles and configuration are first-class: presets let users tune baseline profiles per voice (gender/character) while keeping emotion multipliers consistent. This allows retaining an application-wide emotional intent while adapting stylistic voice differences. Profiles are stored as small JSON/YAML blobs so CI-friendly tests can validate that mappings stay within acceptable ranges during changes.

Safety, calibration, and extensibility are core concerns. Parameters are clamped to perceptually reasonable ranges to avoid distortions, and a simple calibration utility is recommended to map ordinal pitch levels to the numeric scale of any target TTS. The mapping logic is intentionally parametric and data-driven so new emotions, additional intensity tiers, or learned models can be integrated without changing the core runtime pipeline.

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
