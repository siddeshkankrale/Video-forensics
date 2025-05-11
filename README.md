# video-forensics
VidGuard is a forensic tool for verifying the integrity and authenticity of video files. It extracts key metadata, calculates a unique MD5 hash to detect tampering, and analyzes frames for any alterations. VidGuard is ideal for digital forensics, surveillance, compliance auditing, and media verification.

Features Metadata Extraction: Retrieves essential video metadata, including frame count, resolution, and FPS.

File Integrity Check: Calculates an MD5 hash to verify the file’s authenticity.

Frame Analysis: Identifies altered frames by comparing consecutive frames, flagging inconsistencies.

JSON Report Generation: Outputs a comprehensive report in JSON format with all metadata, hash, and frame analysis results.

Installation Clone the repository: bash

Copy code git clone https://github.com/username/VidGuard.git Install required packages: bash Copy code pip install -r requirements.txt Usage Replace sample_video.mp4 with your own video file path, then run: bash Copy code python vidguard.py The analysis report will be saved as report.json in the output folder.

Example Output json Copy code { "metadata": { "frame_count": 500, "frame_width": 1920, "frame_height": 1080, "fps": 30 }, "hash": "9e107d9d372bb6826bd81d3542a419d6", "altered_frames": [15, 20, 25] }

Applications Digital Forensics: Verifying video evidence authenticity. Security Surveillance: Checking footage consistency for tampering. Compliance Auditing: Ensuring unaltered video logs in sensitive environments.

Media Verification: Detecting deepfakes or video modifications.
