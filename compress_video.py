import os
import time
import subprocess
import argparse
from shutil import copytree, ignore_patterns

# Dictionary mapping resolution to height
RESOLUTIONS = {
    "360p": {"width": 640, "height": 360},
    "480p": {"width": 854, "height": 480},
    "720p": {"width": 1280, "height": 720},
    "1080p": {"width": 1920, "height": 1080},
    "2k": {"width": 2560, "height": 1440},
    "4k": {"width": 3840, "height": 2160},
}

CODECS = [
    "h264",
    "h265",
    "vp9",
    "vp8",
    "mpeg4",
    "mpeg2",
    "av1",
    "h264_nvenc",
    "hevc_nvenc",
    "h264_amf",
]


def compress_video(
    source_dir,
    resolution=None,
    preset="medium",
    output_dir="",
    overwrite=False,
    threads=None,
    fps=None,
    codec="h264"
):
    # Create the output directory with timestamp added to the top-level directory name
    parent_dir, dir_name = os.path.split(source_dir)
    timestamp = int(time.time())
    isOutputValidPath = os.path.isdir(output_dir)
    if not isOutputValidPath:
        output_dir = os.path.join(parent_dir, f"{dir_name}_{timestamp}")

    # Only create the output directory if it doesn't already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Compressing {parent_dir} to {output_dir}...")

    # Copy the directory structure from source to output directory
    copytree(source_dir, output_dir, ignore=ignore_patterns("*.*"), dirs_exist_ok=True)

    # Construct the threads option
    threads_option = f"-threads {threads}" if threads is not None else ""

    resolution_str = ""
    if resolution:
        selectedRes = RESOLUTIONS.get(resolution)
        selectedWidth = selectedRes["width"]
        selectedHeight = selectedRes["height"]
        resolution_str = f'-vf "scale={selectedWidth}:{selectedHeight}"'

    # Construct the FPS option
    fps_option = f"-r {fps}" if fps is not None else ""

    # Get list of video files in the source directory and its subdirectories
    video_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith((".mp4", ".avi", ".mov")):
                print(f"Found video file: {file}")
                video_files.append(os.path.join(root, file))

    print(f"Found {len(video_files)} video files to compress...")

    for video_file in video_files:
        # Determine output path
        output_path = os.path.join(output_dir, os.path.relpath(video_file, source_dir))
        output_path_dir = os.path.dirname(output_path)
        os.makedirs(output_path_dir, exist_ok=True)

        # Check if output file exists
        if os.path.exists(output_path):
            if overwrite is False:
                print(f"Output file {output_path} already exists. Skipping...")
                continue
            else:
                print(f"Output file {output_path} already exists. Overwriting...")
                os.remove(output_path)

        # Compress video using FFmpeg with GPU acceleration
        command = f'ffmpeg -i "{video_file}" -c:v {codec} -preset {preset} {resolution_str} {threads_option} {fps_option} "{output_path}"'

        subprocess.run(command, shell=True)
        print(f"Compressing {video_file} to {output_path}...")

    print("Compression complete. Compressed videos are saved in:", output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Compress videos with GPU acceleration using FFmpeg while maintaining directory structure."
    )
    parser.add_argument(
        "--source_dir",
        type=str,
        help="Path to the source directory containing videos to compress",
        required=True,
    )
    parser.add_argument(
        "--output_dir",
        default="",
        type=str,
        help="Path to the output directory to save compressed videos (default: source_dir_timestamp)",
        required=False,
    )
    parser.add_argument(
        "--resolution",
        type=str,
        choices=["360p", "480p", "720p", "1080p", "2k", "4k"],
        help="Resolution of the compressed videos",
        required=False,
    )
    parser.add_argument(
        "--preset",
        type=str,
        choices=[
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
        ],
        default="faster",
        help="Compression preset (default: faster)",
        required=False,
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Whether to overwrite if output files exists",
        required=False,
    )
    parser.add_argument(
        "--delete-once-compressed",
        action="store_true",
        help="Whether to delete the original video files once compressed",
        required=False,
    )

    parser.add_argument(
        "--threads",
        type=int,
        help="Number of threads to use for compression",
        required=False,
    )

    parser.add_argument(
        "--fps",
        type=int,
        help="Frames per second (FPS) for the compressed videos",
        required=False,
    )

    parser.add_argument(
        "--codec",
        type=str,
        choices=CODECS,
        default="h264",
        help="Video codec for compression (default: h264)",
        required=False,
    )
    args = parser.parse_args()

    compress_video(
        args.source_dir,
        args.resolution,
        args.preset,
        args.output_dir,
        args.overwrite,
        args.threads,
        args.fps,
        args.codec
    )


if __name__ == "__main__":
    main()
