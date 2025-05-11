import cv2
import os
import hashlib
import json

# Function to extract video metadata
def extract_metadata(video_path):
    metadata = {}
    cap = cv2.VideoCapture(video_path)
    metadata['frame_count'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    metadata['frame_width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    metadata['frame_height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    metadata['fps'] = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    return metadata

# Function to calculate video file hash (MD5)
def calculate_hash(video_path):
    hash_md5 = hashlib.md5()
    with open(video_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to analyze frames for alterations
def analyze_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    altered_frames = []
    prev_frame = None
    for i in range(frame_count):
        ret, frame = cap.read()
        if ret:
            if prev_frame is not None:
                if not (frame == prev_frame).all():
                    altered_frames.append(i)
            prev_frame = frame.copy()
    cap.release()
    return altered_frames

# Main function
if __name__ == '__main__':
    video_path = 'sample_video.mp4'  # Replace with the path to your video file
    output_folder = 'output'

    # Create an output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract metadata
    metadata = extract_metadata(video_path)
    # Calculate hash
    video_hash = calculate_hash(video_path)
    # Analyze frames for alterations
    altered_frames = analyze_frames(video_path)

    # Create a report
    report = {
        'metadata': metadata,
        'hash': video_hash,
        'altered_frames': altered_frames
    }

    # Save the report as JSON
    report_path = os.path.join(output_folder, 'report.json')
    with open(report_path, 'w') as report_file:
        json.dump(report, report_file, indent=4)

    print('Video forensic analysis complete. Report saved to', report_path)
