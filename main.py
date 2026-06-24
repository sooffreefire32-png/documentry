import os
import datetime
import json
from audio_analyzer import analyze_audio
from scene_engine import generate_scenes
from image_generator import process_all_images
from video_editor import create_video
from seo_scheduler import generate_seo_metadata, get_optimal_publish_time
from config import OUTPUT_DIR, FINAL_VIDEO, TIMELINE_JSON

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
    
    print("✅ Video creation completed successfully!")

    # 5. Prepare SEO Metadata and Scheduling for YouTube
    print("Preparing YouTube SEO metadata and scheduling...")
    transcript = ""
    video_duration_seconds = 0
    if os.path.exists(TIMELINE_JSON):
        with open(TIMELINE_JSON, 'r') as f:
            timeline_data = json.load(f)
            transcript = " ".join([entry['text'] for entry in timeline_data])
            if timeline_data:
                video_duration_seconds = timeline_data[-1]['end'] # Assuming last entry's end is video duration

    seo_metadata = generate_seo_metadata(transcript, video_duration_seconds)
    scheduled_publish_at = get_optimal_publish_time()

    # Save SEO metadata and scheduled time to a file for the YouTube workflow
    seo_data_path = os.path.join(OUTPUT_DIR, "youtube_seo_data.json")
    with open(seo_data_path, 'w') as f:
        json.dump({
            "title": seo_metadata["title"],
            "description": seo_metadata["description"],
            "tags": ",".join(seo_metadata["tags"]),
            "scheduled_publish_at": scheduled_publish_at.isoformat()
        }, f)
    print(f"YouTube SEO data saved to {seo_data_path}")

if __name__ == "__main__":
    run_pipeline()
