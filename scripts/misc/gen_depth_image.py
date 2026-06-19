import OpenEXR
import Imath
import numpy as np
import matplotlib.pyplot as plt
import os

# PROCESS:
# Manually pick photo
# Copy across relative path 
# Change focal parameters 
# Save result into disparity results, in indexed folder
# Move photo into this folder too 

# KEY:
# WATER_CONDITIONS = [ 
#     ("Jerlov",     "Jerlov I",   "Clear"),
#     ("Jerlov.001", "Jerlov IA",  "Clear"),
#     ("Jerlov.005", "Jerlov IB",  "Clear"),
#     ("Jerlov.003", "Jerlov IC",  "Clearish"),  
#     ("Jerlov.004", "Jerlov II",  "Clearish"),
#     ("Jerlov.002", "Jerlov III", "Murky"),
#     ("Jerlov.006", "Jerlov 3C",  "Murky")
#     # ("Jerlov.007", "Jerlov 5C",  "Murky"), # Too murky, can't see anything 
#     # ("Jerlov.008", "Jerlov 7C", "Murky"),      
#     # ("Jerlov.009", "Jerlov 9C", "Murky")
# ]


# Run instructions
# python3 -m venv venve (only first time)
# source venv/bin/activate
# pip install OpenEXR matplotlib
# python3 gen_depth-image.py

def read_exr_channel(exr_path, channel='R'):
    """Read a single channel from an EXR file as a float32 numpy array."""
    exr_file = OpenEXR.InputFile(exr_path)
    header = exr_file.header()
    dw = header['dataWindow']
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    ch_str = exr_file.channel(channel, pt)
    ch = np.frombuffer(ch_str, dtype=np.float32)
    ch.shape = (height, width)
    return ch


def process_depth_exr_disparity(input_path, output_path, f_pixels, baseline_m, max_depth=1.95):
    """Convert depth EXR to disparity visualization. Depth > max_depth → black."""

    depth = read_exr_channel(input_path, channel='R')
    # depth = np.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0)
    depth = np.nan_to_num(depth, nan=np.inf, posinf=np.inf, neginf=np.inf)

    # Debugging
    # print("min depth:", depth.min())
    # print("max depth:", depth.max())
    # print("pixels < 1.95:", np.sum(depth < 1.95))

    # Mask far pixels
    mask = depth > max_depth

    # Avoid divide by zero
    depth[depth <= 0] = 1e-6

    # Disparity
    disparity = (f_pixels * baseline_m) / depth

    # Set masked pixels to black
    disparity[mask] = np.nan
    cmap = plt.cm.Spectral_r.copy()
    cmap.set_bad(color='black')

    # Save directly
    plt.imsave(output_path, disparity, cmap=cmap) # 'Spectral_r')
    plt.imsave(output_path, disparity, cmap=cmap,
           vmin=0, vmax=np.nanmax(disparity))


# ---- Paths ----
script_dir = os.path.dirname(os.path.abspath(__file__))

# ---- Explicit input files ----
left_exr = "scripts/misc/disparity_results/app_jerlov_IB_f25_i004_shallow/raw depth0010_R.exr"
left_output = os.path.join(script_dir, "disparity_results/app_jerlov_IB_f25_i004_shallow/right_disparity_vis.png")

# ---- Blender camera parameters ----
f_mm = 1.5                 # Blender focal length in mm
sensor_width_mm = 6.7      # Blender camera sensor width in mm
render_width_px = 640       # image width in pixels

# Convert focal length to pixels
f_pixels = f_mm * (render_width_px / sensor_width_mm)
baseline_m = 0.04

# ---- Process ----
process_depth_exr_disparity(left_exr, left_output, f_pixels, baseline_m)

print("Done! Disparity visualizations saved as:", left_output)
