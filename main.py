import os
from audio_analyzer import analyze_audio
from scene_engine import generate_scenes
from image_generator import process_all_images
from video_editor import create_video
from config import OUTPUT_DIR

def run_pipeline():
    print("🚀 Starting AI Documentary Automation Pipeline")
    
    # 1. Analyze Audio
    if not analyze_audio():
        print("Audio analysis failed. Exiting.")
        return

    # 2. Generate Scenes
    scenes = generate_scenes()
    if not scenes:
        print("Scene generation failed. Exiting.")
        return

    # 3. Generate Images via Cloudflare
    image_map = process_all_images(scenes)
    if not image_map:
        print("Image generation failed. Exiting.")
        return

    # 4. Assemble Video
    create_video(scenes, image_map)
    
    print("✅ Pipeline execution completed successfully!")

if __name__ == "__main__":
    run_pipeline()
