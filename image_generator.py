import requests
import os
import time
from config import CLOUDFLARE_API_KEY, CLOUDFLARE_API_URL, IMAGE_OUTPUT_DIR

def generate_image(prompt, scene_id):
    print(f"Generating image for scene {scene_id}...")
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"{prompt}, cinematic documentary style, high resolution, 8k",
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(CLOUDFLARE_API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                image_path = os.path.join(IMAGE_OUTPUT_DIR, f"scene_{scene_id:03d}.png")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return image_path
            else:
                print(f"Attempt {attempt + 1} failed with status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
        time.sleep(2)
    
    return None

def process_all_images(scenes):
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
    image_map = {}
    for scene in scenes:
        path = generate_image(scene['prompt'], scene['id'])
        if path:
            image_map[scene['id']] = path
    return image_map
