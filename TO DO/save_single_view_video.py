# Save rendered animation images as a video 
# For a single view (not stereo)
# Does left view of raw image
# Select left or right, or raw image, raw depth or normalised depth

# --- RUN INSTRUCTIONS ---
# Run file from VS Code
# Check FPS, image selection for desired settings

# Import libraries 
import cv2
import glob
import os

# Define source of images 
base_folder = "/home/otur3695/Documents/Blender/results/orbit 240 frames"
# base_folder = "/home/otur3695/Documents/Blender/results/orbit 240 frames/delete_global"


# Make video folder to save into 
video_folder = os.path.join(base_folder, "single view videos")
os.makedirs(video_folder, exist_ok=True)

# Define desired FPS 
fps = 24

# Define mp4 format 
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Select image type 
image_type = "raw image*_L.jpg"
video_name = "raw_image_L"

# "raw image*_L.jpg"
# "raw image*_R.jpg"
# "raw depth*_L.tif"
# "raw depth*_L.tif"
# "normalized depth*_L.tif"
# "normalized depth*_R.tif"
# image_type = "0*_L.jpg"
# video_name = "global_image_L"
 
# Find frames
frames = sorted(glob.glob(os.path.join(base_folder, image_type)))

print(f"Found {len(frames)} frames")

if len(frames) == 0:
    raise RuntimeError("No frames found")

# Read first frame to get size
img = cv2.imread(frames[0])
h, w, _ = img.shape
out_size = (w, h)

# Video writer
out_path = os.path.join(video_folder, f"{video_name}_single view.mp4")
writer = cv2.VideoWriter(out_path, fourcc, fps, out_size)

# Read and save each frame to video
for fname in frames:
    img = cv2.imread(fname)
    if img is None:
        continue

    writer.write(img)  

writer.release()

print(f"Saved video to: {out_path}")
