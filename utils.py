import cv2
import hashlib
import numpy as np
import os

def extract_metadata(video_path):
    """
    Extract video metadata including frame count, width, height, FPS, and codec
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        dict: Dictionary containing video metadata
    """
    metadata = {}
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return {"error": "Failed to open video file"}
    
    # Extract basic metadata
    metadata['frame_count'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    metadata['frame_width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    metadata['frame_height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    metadata['fps'] = cap.get(cv2.CAP_PROP_FPS)
    metadata['resolution'] = f"{metadata['frame_width']}x{metadata['frame_height']}"
    
    # Get codec information
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    # Convert fourcc to human-readable format
    fourcc_chars = chr(fourcc_int & 0xFF) + chr((fourcc_int >> 8) & 0xFF) + chr((fourcc_int >> 16) & 0xFF) + chr((fourcc_int >> 24) & 0xFF)
    metadata['codec'] = fourcc_chars
    
    # Calculate duration
    if metadata['fps'] > 0:
        metadata['duration_seconds'] = metadata['frame_count'] / metadata['fps']
    else:
        metadata['duration_seconds'] = 0
    
    cap.release()
    return metadata

def calculate_hash(video_path):
    """
    Calculate MD5 hash of the video file
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        str: MD5 hash of the video file
    """
    hash_md5 = hashlib.md5()
    with open(video_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def analyze_frames(video_path, threshold=0.05):
    """
    Analyze frames for alterations or tampering
    
    Args:
        video_path (str): Path to the video file
        threshold (float): Threshold for frame difference detection
        
    Returns:
        list: List of potentially altered frame indices
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if frame_count <= 0:
        return []
    
    altered_frames = []
    prev_frame = None
    
    for i in range(frame_count):
        ret, frame = cap.read()
        
        if not ret:
            break
            
        # Convert to grayscale for easier comparison
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            # Calculate difference between current and previous frame
            diff = cv2.absdiff(gray_frame, prev_frame)
            
            # Calculate percentage of changed pixels
            change_percentage = np.count_nonzero(diff > 25) / diff.size
            
            # Detect sudden changes that could indicate tampering
            if change_percentage > threshold:
                altered_frames.append(i)
        
        prev_frame = gray_frame
        
    cap.release()
    return altered_frames
