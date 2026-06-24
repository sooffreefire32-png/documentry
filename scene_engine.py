import json
import os
from config import TIMELINE_JSON, IMAGE_PROMPTS

def generate_scenes():
    print("Generating scenes...")
    if not os.path.exists(TIMELINE_JSON):
        print(f"Error: {TIMELINE_JSON} not found.")
        return None

    with open(TIMELINE_JSON, 'r') as f:
        timeline = json.load(f)
    
    with open(IMAGE_PROMPTS, 'r') as f:
        prompts = [line.strip() for line in f.readlines() if line.strip()]

    scenes = []
    prompt_idx = 0
    
    for i, entry in enumerate(timeline):
        # Assign a prompt to each scene segment
        prompt = prompts[prompt_idx % len(prompts)]
        prompt_idx += 1
        
        # Decide if main character should be shown (e.g., every 3rd scene or based on timing)
        show_character = (i % 3 == 0)
        
        scenes.append({
            "id": i + 1,
            "start": entry['start'],
            "end": entry['end'],
            "text": entry['text'],
            "prompt": prompt,
            "show_character": show_character,
            "scene_type": "mystery" if i % 2 == 0 else "evidence"
        })
    
    print(f"Generated {len(scenes)} scenes.")
    return scenes

if __name__ == "__main__":
    generate_scenes()
