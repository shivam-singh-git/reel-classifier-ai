import cv2

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
