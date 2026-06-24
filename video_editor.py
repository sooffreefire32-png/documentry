import os
import subprocess
import json
from config import SCRIPT_AUDIO, MAIN_CHARACTER_VIDEO, FINAL_VIDEO, IMAGE_OUTPUT_DIR, TEMP_DIR

def create_concat_file(scenes, image_map):
    concat_file_path = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_file_path, "w") as f:
        for scene in scenes:
            img_path = image_map.get(scene["id"])
            if img_path:
                f.write(f"file '{img_path}'\n")
                f.write(f"duration {scene['end'] - scene['start']}\n")
    return concat_file_path

def apply_ken_burns(input_image, output_video, duration):
    # Simplified Ken Burns effect: zoom in from top-left to bottom-right
    # This is a basic example, more complex effects would require more parameters
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", input_image,
        "-vf", f"zoompan=z='min(zoom+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s='1920x1080',fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5",
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-y", output_video
    ]
    subprocess.run(cmd, check=True)

def create_video(scenes, image_map):
    print("Starting professional video assembly with FFmpeg...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    processed_video_segments = []
    for scene in scenes:
        img_path = image_map.get(scene["id"])
        if img_path:
            duration = scene["end"] - scene["start"]
            output_segment_path = os.path.join(TEMP_DIR, f"segment_{scene['id']:03d}.mp4")
            
            # Apply Ken Burns effect to each image segment
            try:
                apply_ken_burns(img_path, output_segment_path, duration)
                processed_video_segments.append(output_segment_path)
            except subprocess.CalledProcessError as e:
                print(f"Error applying Ken Burns to {img_path}: {e}")
                # Fallback to simple image display if Ken Burns fails
                cmd = [
                    "ffmpeg",
                    "-loop", "1",
                    "-i", img_path,
                    "-t", str(duration),
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-y", output_segment_path
                ]
                subprocess.run(cmd, check=True)
                processed_video_segments.append(output_segment_path)

    # Create a concat list for FFmpeg
    concat_list_path = os.path.join(TEMP_DIR, "final_concat_list.txt")
    with open(concat_list_path, "w") as f:
        for segment in processed_video_segments:
            f.write(f"file '{segment}'\n")

    # Concatenate all video segments and add audio
    final_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-i", SCRIPT_AUDIO,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", FINAL_VIDEO
    ]
    
    print(f"Executing final FFmpeg command: {' '.join(final_cmd)}")
    try:
        subprocess.run(final_cmd, check=True)
        print(f"Final video created at {FINAL_VIDEO}")
    except subprocess.CalledProcessError as e:
        print(f"Error during final video creation: {e}")
        print(f"FFmpeg stderr: {e.stderr.decode()}")

if __name__ == "__main__":
    # Placeholder for local testing - requires dummy data
    pass
