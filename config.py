import os

# GitHub and API Configuration
GH_TOKEN = os.environ.get("GH_TOKEN")
CLOUDFLARE_API_KEY = os.environ.get("CLOUDFLARE_API_KEY")
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_URL = "https://aiimagegenerationapi.sooffreefire32.workers.dev/"

# Paths
ASSETS_DIR = "assets"
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "images")

# File Names
SCRIPT_AUDIO = os.path.join(ASSETS_DIR, "script.mp3")
IMAGE_PROMPTS = os.path.join(ASSETS_DIR, "image_prompts.txt")
MAIN_CHARACTER_VIDEO = os.path.join(ASSETS_DIR, "main_character.mp4")
TIMELINE_JSON = os.path.join(TEMP_DIR, "timeline.json")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_video.mp4")

# Scene Settings
MIN_SCENE_DURATION = 2
MAX_SCENE_DURATION = 6
