# Check Blender raw depth values approximately align with the expected depth measured in Blender

# --- RUN INSTRUCTIONS --- 
# Run file in VS Code
# Can change file path names, dot radius and query pixel
# Outputs saved image

# --- TO DO ---
# Working with .exr, try again with .tif? 
# Change to just use raw depth and not normalised? 

import cv2
import numpy as np

# Define input/output image filepaths
raw_depth_path = "datasets/demo/depth_check/input/raw depth0001_L.exr"  # "raw depth0001_L.exr"                  # Raw EXR depth for depth value
normalized_depth_path = "datasets/demo/depth_check/input/normalized depth0001_L.tif"  # "normalized depth0001_L.tif"    # Normalised depth just to draw on (easier to see then raw depth)
output_image = "datasets/demo/depth_check/output/normalized_depth_with_marker.png"       # Output image name 

# Define query pixel (x, y)
# check_pixel = (505, 255)                       # Front left middle pole
check_pixel = (450, 215)                         # Back left middle pole

# Load in raw depth image
raw_depth = cv2.imread(raw_depth_path, cv2.IMREAD_UNCHANGED)
if raw_depth is None:
    raise RuntimeError(f"Could not read raw depth file: {raw_depth_path}")

# Extract first channel of .exr (has 4 channels)
if raw_depth.ndim == 3:
    raw_depth = raw_depth[:, :, 0]

# Extract x, y query pixel and image height and width
x, y = check_pixel
h, w = raw_depth.shape
if not (0 <= x < w and 0 <= y < h):
    raise RuntimeError(f"Pixel {check_pixel} out of bounds ({w}x{h})")

# Extract depth value at that query pixel 
depth_value = raw_depth[y, x]
print(f"Depth at pixel {check_pixel} from raw EXR depth: {depth_value}")


# Load in normalised depth image 
norm_img = cv2.imread(normalized_depth_path, cv2.IMREAD_UNCHANGED)
if norm_img is None:
    raise RuntimeError(f"Could not read normalized depth image: {normalized_depth_path}")

# Convert normalised depth to BGR (if single channel)
if norm_img.ndim == 2:
    norm_img = cv2.cvtColor(norm_img, cv2.COLOR_GRAY2BGR)

# Draw red dot for query pixel onto normalised depth image
dot_radius = 6
cv2.circle(
    norm_img,
    (x, y),
    dot_radius,
    (0, 0, 255),  # red in BGR
    -1
)

# Save the normalised depth image with query pixel drawn on 
cv2.imwrite(output_image, norm_img)
print(f"Saved annotated normalized depth image to: {output_image}")













# # FOR .TIF BUT DEPTHVALUE FROM PIXELS WERE WRONG
# import cv2
# import numpy as np
# import os

# # -----------------------------
# # CONFIG
# # -----------------------------
# depth_path = "raw depth0001_L.tif"        # relative path
# check_pixel = (505, 255)                 # (x, y)
# dot_radius = 3

# output_image = "raw_depth_with_marker.png"

# # -----------------------------
# # LOAD DEPTH IMAGE
# # -----------------------------
# depth = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)

# if depth is None:
#     raise RuntimeError(f"Could not read depth file: {depth_path}")

# depth = depth.astype(np.float32)

# # -----------------------------
# # NORMALIZE FOR DISPLAY
# # -----------------------------
# depth_vis = cv2.normalize(
#     depth, None, 0, 255, cv2.NORM_MINMAX
# ).astype(np.uint8)

# depth_vis = cv2.cvtColor(depth_vis, cv2.COLOR_GRAY2BGR)

# # -----------------------------
# # DRAW RED DOT
# # -----------------------------
# x, y = check_pixel
# h, w = depth_vis.shape[:2]

# if not (0 <= x < w and 0 <= y < h):
#     raise RuntimeError(f"Pixel {check_pixel} out of bounds ({w}x{h})")

# cv2.circle(
#     depth_vis,
#     (x, y),
#     dot_radius,
#     (0, 0, 255),   # red
#     -1
# )

# # -----------------------------
# # PRINT DEPTH VALUE
# # -----------------------------
# depth_value = depth[y, x]
# print(f"Depth value at pixel {check_pixel}: {depth_value}")

# # -----------------------------
# # SAVE IMAGE
# # -----------------------------
# cv2.imwrite(output_image, depth_vis)
# print(f"Saved annotated image to: {output_image}")

