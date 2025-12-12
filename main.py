import argparse
import glob
import os
import cv2


def get_image_files(input_folder: str) -> list[str]:
    """Get all image files from the input folder, sorted by name."""
    image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff", "*.tif", "*.webp"]
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        image_files.extend(glob.glob(os.path.join(input_folder, ext.upper())))
    
    return sorted(image_files)


def frames_to_video(input_folder: str, output_path: str, fps: int) -> None:
    """Combine image frames from input folder into a video."""
    image_files = get_image_files(input_folder)
    
    if not image_files:
        print(f"No image files found in '{input_folder}'")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Read the first image to get dimensions
    first_frame = cv2.imread(image_files[0])
    if first_frame is None:
        print(f"Could not read image: {image_files[0]}")
        return
    
    height, width, _ = first_frame.shape
    print(f"Video dimensions: {width}x{height}")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write all frames to video
    for i, image_path in enumerate(image_files):
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Warning: Could not read image {image_path}, skipping...")
            continue
        
        # Resize if dimensions don't match the first frame
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))
        
        video_writer.write(frame)
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(image_files)} frames")
    
    video_writer.release()
    print(f"Video saved to '{output_path}'")
    print(f"Duration: {len(image_files) / fps:.2f} seconds at {fps} FPS")


def main():
    parser = argparse.ArgumentParser(
        description="Combine image frames into a video"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default="input",
        help="Input folder containing image frames (default: input)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output video file path (default: output/video-{fps}.mp4)"
    )
    parser.add_argument(
        "--fps", "-f",
        type=int,
        default=30,
        help="Frames per second (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Set default output path with fps in filename
    if args.output is None:
        args.output = f"output/video-{args.fps}.mp4"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    frames_to_video(args.input, args.output, args.fps)


if __name__ == "__main__":
    main()
