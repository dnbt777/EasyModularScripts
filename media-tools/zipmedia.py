import subprocess
import argparse
import os

def is_image(file_path):
    return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'))

def is_video(file_path):
    return file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm', '.gif'))

def create_video_from_image(image_path, video_path, duration):
    ffmpeg_command = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-pix_fmt', 'yuv420p',
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        '-y',  # Overwrite output file if it exists
        video_path
    ]
    subprocess.run(ffmpeg_command, check=True)

def get_video_duration(video_path):
    ffmpeg_command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def get_video_height(video_path):
    ffmpeg_command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=height',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return int(result.stdout.strip())

def combine_gifs_side_by_side(media1_path, media2_path, output_path):
    temp_video1 = 'temp_video1.mp4'
    temp_video2 = 'temp_video2.mp4'

    if is_image(media1_path) and is_video(media2_path):
        duration = get_video_duration(media2_path)
        create_video_from_image(media1_path, temp_video1, duration)
        media1_path = temp_video1
    elif is_video(media1_path) and is_image(media2_path):
        duration = get_video_duration(media1_path)
        create_video_from_image(media2_path, temp_video2, duration)
        media2_path = temp_video2

    # Get the height of the first video
    height1 = get_video_height(media1_path)
    height2 = get_video_height(media2_path)
    target_height = min(height1, height2)

    # Construct the ffmpeg command with scaling to match heights
    ffmpeg_command = [
        'ffmpeg',
        '-i', media1_path,
        '-i', media2_path,
        '-filter_complex', f'[0:v]scale=-1:{target_height}[vid1];[1:v]scale=-1:{target_height}[vid2];[vid1][vid2]hstack=inputs=2[v]',
        '-map', '[v]',
        '-y',  # Overwrite output file if it exists
        output_path
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Combined media saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining videos: {e}")
    finally:
        if os.path.exists(temp_video1):
            os.remove(temp_video1)
        if os.path.exists(temp_video2):
            os.remove(temp_video2)

def main():
    parser = argparse.ArgumentParser(description="Combine two media files side by side.")
    parser.add_argument('media1', help="Path to the first media file (x.png, y.gif, etc)")
    parser.add_argument('media2', help="Path to the second media file")
    parser.add_argument('output', help="Path+format to save the combined video (name.output_format)")

    args = parser.parse_args()

    combine_gifs_side_by_side(args.media1, args.media2, args.output)

if __name__ == "__main__":
    main()

