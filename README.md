# AI Documentary Video Automation System

This repository contains a fully automated, production-grade pipeline that generates cinematic documentary videos from minimal inputs using AI.

## 🎯 System Goal
Automatically convert narration audio and image prompts into a high-quality cinematic documentary video with perfect audio sync, AI-generated images, and professional transitions.

## 🧠 Architecture
1. **Audio Analysis**: Uses Whisper to transcribe and timestamp the narration.
2. **Scene Generation**: Segments the video based on the audio timeline and assigns visual prompts.
3. **Image Generation**: Calls the Cloudflare AI API to generate cinematic images for each scene.
4. **Video Editing**: Uses FFmpeg to assemble the images, overlays, and audio into a final MP4.

## 🚀 Usage
1. Place your assets in the `assets/` directory:
   - `script.mp3`: Narration audio.
   - `image_prompts.txt`: List of visual prompts.
   - `main_character.mp4`: A 5-second loopable video of the main character.
2. Configure GitHub Secrets:
   - `GH_TOKEN`: Your GitHub Personal Access Token.
   - `CLOUDFLARE_API_KEY`: Your Cloudflare API Token.
   - `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare Account ID.
3. Push to the `main` branch to trigger the automation pipeline.

## 🛠 Technology Stack
- **Python**: Core logic and orchestration.
- **Whisper**: Audio transcription and analysis.
- **Cloudflare AI**: Image generation.
- **FFmpeg**: Video rendering and editing.
- **GitHub Actions**: CI/CD automation.
