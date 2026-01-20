# Output Blender raw depth value at query pixel
# Used to check if they approximately/qualitatively align with the expected depth measured in Blender (with ruler tool)

# --- INPUTS ---
# External files: Raw depth and raw image files in demos/depth_check/inputs folder 
# Variables: File path names and query pixel

# --- OUTPUTS ---
# Depth at query pixel (printed to terminal)
# Raw image with query pixel indicated (red circle)

# --- RUN INSTRUCTIONS --- 
# python3 scripts/misc/check_depth.py from the repo root 

# --- TO DO ---
# Replace input files 


# Import libraries
import cv2
import numpy as np

# Define input/output image filepaths
raw_depth_path = "demos/check_depth/input/raw depth0001_L.exr"                    # Raw EXR depth for depth value
raw_image_path = "demos/check_depth/input/raw image0001_L.jpg"                    # Raw image for visualising query pixel
output_image = "demos/check_depth/output/raw_image_with_marker.jpg"               # Output image name 

# Define query pixel (x, y)
check_pixel = (505, 255)                       # Front left middle pole
# check_pixel = (450, 215)                       # Back left middle pole

# Load in raw depth image - IMREAD_UNCHANGED to preserve raw depth details
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
print(f"Depth at pixel {check_pixel} from raw EXR depth: {depth_value}m")

# Load in raw image (for visualisation)
raw_image = cv2.imread(raw_image_path)
# raw_image = cv2.cvtColor(cv2.imread(raw_image_path), cv2.COLOR_BGR2RGB)

# Draw circle and fill
dot_radius = 6
cv2.circle(
    raw_image,
    (x, y),
    dot_radius,
    (0, 0, 255),  # red
    -1            # fill in circle
)

# Save image to output folder 
cv2.imwrite(output_image, raw_image)
print(f"Saved annotated raw image to: {output_image}")
