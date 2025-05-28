import requests

def download_video_from_url(video_url: str, output_path: str) -> str:
    """
    Downloads a video from the given URL and saves it locally.
    
    Args:
        video_url (str): Direct URL to .mp4 file
        output_path (str): Local filename to save it (e.g. 'reel.mp4')
    
    Returns:
        str: Path to the saved video file
    """
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return output_path
    else:
        raise Exception(f"Failed to download video: {response.status_code}")


download_video_from_url("https://www.instagram.com/reel/DJU3A57Rb7D/?utm_source=ig_web_copy_link", "reel.mp4")