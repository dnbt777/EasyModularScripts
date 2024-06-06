import subprocess
import argparse

def combine_gifs_side_by_side(gif1_path, gif2_path, output_path):
    # Construct the ffmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-i', gif1_path,
        '-i', gif2_path,
        '-filter_complex', '[0:v][1:v]hstack=inputs=2[v]',
        '-map', '[v]',
        '-y',  # Overwrite output file if it exists
        output_path
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Combined video saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining videos: {e}")

def main():
    parser = argparse.ArgumentParser(description="Combine two videos side by side.")
    parser.add_argument('gif1', help="Path to the first video")
    parser.add_argument('gif2', help="Path to the second video")
    parser.add_argument('output', help="Path to save the combined video")

    args = parser.parse_args()

    combine_gifs_side_by_side(args.gif1, args.gif2, args.output)

if __name__ == "__main__":
    main()
