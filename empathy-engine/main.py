# main.py

import os
import argparse
from flask import Flask, render_template, request, jsonify
from app.emotion_analyzer import detect_emotion
from app.voice_engine import generate_speech

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            return render_template("index.html", error="Please enter some text.")
        
        emotion = detect_emotion(text)
        audio_file = os.path.basename(generate_speech(text, emotion))
        return render_template("index.html", input_text=text, emotion=emotion, audio_file=audio_file)
    
    return render_template("index.html")

def run_cli():
    print("🎙️ The Empathy Engine - CLI Mode")
    text = input("Enter your text: ").strip()
    if not text:
        print("❌ No text provided.")
        return
    
    print("🔍 Analyzing emotion...")
    emotion = detect_emotion(text)
    print(f"💡 Detected emotion: {emotion}")
    
    print("🔊 Generating speech...")
    audio_path = generate_speech(text, emotion)
    print(f"✅ Audio saved to: {audio_path}")
    print("🎧 Play the file to hear the empathetic voice!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode instead of web server")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        print("🚀 Starting web server at http://localhost:5000")
        app.run(debug=True)