import os
import subprocess
import concurrent.futures
from config import SCRIPT_AUDIO, FINAL_VIDEO, TEMP_DIR

def apply_ken_burns(input_image, output_video, duration):
    # Optimized Ken Burns effect with faster preset
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", input_image,
        "-vf", f"zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s='1920x1080',fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-y", output_video
    ]
    subprocess.run(cmd, check=True, capture_output=True)

def process_segment(scene, image_map):
    img_path = image_map.get(scene["id"])
    if not img_path:
        return None
    
    duration = scene["end"] - scene["start"]
    output_segment_path = os.path.join(TEMP_DIR, f"segment_{scene['id']:03d}.mp4")
    
    if os.path.exists(output_segment_path):
        return output_segment_path

    try:
        apply_ken_burns(img_path, output_segment_path, duration)
        return output_segment_path
    except Exception as e:
        print(f"Error processing scene {scene['id']}: {e}")
        return None

def create_video(scenes, image_map):
    print(f"Starting optimized video assembly for {len(scenes)} scenes...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Use ThreadPoolExecutor for parallel segment processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_segment, scene, image_map) for scene in scenes]
        processed_video_segments = [f.result() for f in futures if f.result() is not None]

    if not processed_video_segments:
        print("No video segments were processed successfully.")
        return

    # Create a concat list for FFmpeg
    concat_list_path = os.path.join(TEMP_DIR, "final_concat_list.txt")
    with open(concat_list_path, "w") as f:
        for segment in processed_video_segments:
            f.write(f"file '{os.path.abspath(segment)}'\n")

    # Concatenate all video segments and add audio
    final_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-i", SCRIPT_AUDIO,
        "-c:v", "copy",  # Copy codec since segments are already encoded
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", FINAL_VIDEO
    ]
    
    print(f"Executing final FFmpeg command...")
    try:
        subprocess.run(final_cmd, check=True, capture_output=True)
        print(f"Final video created successfully at {FINAL_VIDEO}")
    except subprocess.CalledProcessError as e:
        print(f"Error during final video creation: {e.stderr.decode()}")

if __name__ == "__main__":
    pass
