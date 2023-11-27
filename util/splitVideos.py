import cv2
import argparse
import os

DESCRIPTION = "Parses the metadata from a given tflite and exports it as JSON"
EXPORT_DIR = "./frames"

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("filename",
        help="path to video file")
parser.add_argument("frameskip",
		help="number of frames to skip between saving",
		type=int)
args = parser.parse_args()

if not os.path.isdir(EXPORT_DIR):
    print("Creating export directory...")
    os.mkdir(EXPORT_DIR)

# Function to extract frames 
import cv2
import os

def extract_frames(video_path: str, skip_frames: int):

   # Open the video file
   video = cv2.VideoCapture(video_path)

   # Get the total number of frames in the video
   total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

   # Set up a counter to keep track of the frames we've extracted
   counter = 0

   # Print info
   print("Splitting video with following parameters:")
   print("File: "+args.filename)
   print("Frame skip: "+args.frame)
   print("--- Video Info ---")
   print("Path: "+video_path)
   print("Total # of Frames: "+total_frames)

   # Loop through the frames of the video
   while True:
       # Read the next frame
       ret, frame = video.read()

       # Check if we've reached the end of the video
       if not ret:
           break

       # Only save the frame if it's one of the frames we want to keep
       if counter % skip_frames == 0:
           # Save the frame to a file
           cv2.imwrite(os.path.join(EXPORT_DIR, f"frame_{counter}.jpg"), frame)

       # Increment the counter
       counter += 1

   # Release the video capture
   video.release()


# Driver Code 
if __name__ == '__main__': 

	# Usage
	extract_frames(args.filename, args.frameskip)
