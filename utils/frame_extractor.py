import cv2
import os

def extract_first_frame(video_path: str, output_image_path: str) -> str:
    """
    Extracts the first frame from a video using OpenCV and saves it as an image.

    Args:
        video_path (str): Path to the input video file (e.g. .mp4)
        output_image_path (str): Path to save the extracted image (e.g. .jpg)

    Returns:
        str: Path to the saved image
    """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise Exception(f"Cannot open video file: {video_path}")

    success, frame = cap.read()
    if not success:
        cap.release()
        raise Exception("Failed to read the first frame from the video.")

    cv2.imwrite(output_image_path, frame)
    cap.release()

    return output_image_path



def extract_keyframes(video_path, output_dir="temp/frames", frame_count=4):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total_frames // frame_count, 1)

    saved = []
    for i in range(frame_count):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if not ret:
            continue
        frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
        cv2.imwrite(frame_path, frame)
        saved.append(frame_path)

    cap.release()
    return saved
