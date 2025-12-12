# frame2video

Convert image frames into a video.

## Usage

```bash
uv run main.py --fps 30
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--input` | `-i` | `input` | Input folder containing image frames |
| `--output` | `-o` | `output/video-{fps}.mp4` | Output video file path |
| `--fps` | `-f` | `30` | Frames per second |

## Supported Formats

PNG, JPG, JPEG, BMP, TIFF, TIF, WEBP
