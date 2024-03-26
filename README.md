# Video Compression Script

This script allows you to compress video files using FFmpeg with GPU acceleration while maintaining directory structure.

## Requirements

- Python 3.x
- FFmpeg installed and added to system PATH

## Installation

1. Clone this repository or download the script file (`compress_video.py`) to your local machine.

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```


## Usage
Run the script from the command line with the following options:

```bash
python compress_video.py --source_dir SOURCE_DIR [options]
```




## Options
--source_dir: Path to the source directory containing videos to compress (required).

--output_dir: Path to the output directory to save compressed videos. Default: SOURCE_DIR_TIMESTAMP.

--resolution: Resolution of the compressed videos (e.g., 360p, 480p, 720p, 1080p, 2k, 4k).

--preset: Compression preset (e.g., ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow). Default: faster.

--overwrite: Whether to overwrite if output files exist (boolean).

--delete-once-compressed: Whether to delete the original video files once compressed (boolean).

--threads: Number of threads to use for compression.

--fps: Frames per second (FPS) for the compressed videos.

--codec: Video codec for compression (e.g., h264, h265, vp9, vp8, mpeg4, mpeg2, av1, h264_nvenc, hevc_nvenc, h264_amf). Default: h264.

## Example

```bash
python compress_video.py --source_dir /path/to/source --resolution 720p --preset medium --output_dir /path/to/output --delete-once-compressed
```


This will compress videos in the specified source directory to 720p resolution using the medium preset, save the compressed videos to the specified output directory, and delete the original video files once compressed.
