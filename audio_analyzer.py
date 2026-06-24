import os
import json
import whisper
from config import SCRIPT_AUDIO, TIMELINE_JSON

def analyze_audio():
    print("Starting audio analysis...")
    if not os.path.exists(SCRIPT_AUDIO):
        print(f"Error: {SCRIPT_AUDIO} not found.")
        return False

    model = whisper.load_model("base")
    result = model.transcribe(SCRIPT_AUDIO, verbose=False)
    
    timeline = []
    for segment in result['segments']:
        timeline.append({
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'].strip()
        })
    
    os.makedirs(os.path.dirname(TIMELINE_JSON), exist_ok=True)
    with open(TIMELINE_JSON, 'w') as f:
        json.dump(timeline, f, indent=4)
    
    print(f"Audio analysis complete. Timeline saved to {TIMELINE_JSON}")
    return True

if __name__ == "__main__":
    analyze_audio()
