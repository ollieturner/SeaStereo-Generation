# Save rendered animation images as a video
# For stereo view - saves left and right images 
# Does raw image, raw depth and normalised depth 

# --- RUN INSTRUCTIONS ---
# Run file from VS Code
# Check FPS and PASSES for desired settings 

# --- TO DO ---
# Automate to iterate over different folder names
# Customise output filepath 


# Import libraries
import cv2
import glob
import os

# Define source of images 
base_folder = "/home/otur3695/Documents/Blender/results/orbit 240 frames"

# Make video folder to save into 
video_folder = os.path.join(base_folder, "videos")
os.makedirs(video_folder, exist_ok=True)

# Define desired FPS 
fps = 24

# Define mp4 format 
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Define files to process (raw image, raw depth and normalised depth)
# key = name for output video
# pattern = prefix before _L / _R in filename from Blender output
PASSES = {
    "raw_image": {
        "L": "raw image*_L.jpg",
        "R": "raw image*_R.jpg",
    },
    "raw_depth": {
        "L": "raw depth*_L.tif",
        "R": "raw depth*_L.tif",
    },
    "normalized_depth": {
        "L": "normalized depth*_L.tif",
        "R": "normalized depth*_R.tif",
    },
}

# Process each pass
for pass_name, patterns in PASSES.items():
    print(f"\n=== Processing pass: {pass_name} ===")

    # Extract L and R images
    L = sorted(glob.glob(os.path.join(base_folder, patterns["L"])))
    R = sorted(glob.glob(os.path.join(base_folder, patterns["R"])))

    # Check if images extracted correctly
    if len(L) == 0 or len(L) != len(R):
        print(f"Skipping {pass_name}: no matching frames")
        continue

    # Read in first L/R image
    img_l = cv2.imread(L[0])
    img_r = cv2.imread(R[0])

    if img_l is None or img_r is None:
        print(f"Skipping {pass_name}: failed to read first frame")
        continue

    # Extract image information (height, width, output size of L/R side-by-side)
    h, w, _ = img_l.shape
    out_size = (w * 2, h)

    # Define output path and writer object
    out_path = os.path.join(video_folder, f"{pass_name}_stereo.mp4")
    writer = cv2.VideoWriter(out_path, fourcc, fps, out_size)

    # Process each image and add into video 
    for l, r in zip(L, R):
        img_l = cv2.imread(l)
        img_r = cv2.imread(r)
        if img_l is None or img_r is None:
            continue

        stereo = cv2.hconcat([img_l, img_r])
        writer.write(stereo)

    writer.release()
    print(f"Saved video: {out_path}")

print("\nAll passes processed.")

