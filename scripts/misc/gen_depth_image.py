import OpenEXR
import Imath
import numpy as np
import matplotlib.pyplot as plt
import os

# TO DO:
# Pick out 6 more photos
# Redo all photos there
# Redo diagram photo
# Convert all to pdfs

# Upload into table
# Push all files
# Switch to windows and update diagram 

# Check blender for headless test run 


# OLD:
# Clear shallow --> Jerlov IA, Arc camera
# Clear deep --> Jerlov I, Orbit camera
# Clearish shallow --> Jerlov IB, Approach
# Clearish deep --> Jerlov IB, Orbit
# Clear-murky shallow --> Jerlov IC, Arc
# Clear-murky deep --> Jerlov II, Orbit
# Murky --> Jerlov 3C, app
# Murky --> Jerlov III, arc


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
left_exr = "for_diagram/orig_raw depth0001_R.exr"
left_output = os.path.join(script_dir, "for_diagram/right_disparity_vis.png")


# ---- Blender camera parameters ----
f_mm = 1.5                 # Blender focal length in mm
sensor_width_mm = 6.7      # Blender camera sensor width in mm
render_width_px = 640       # image width in pixels

# Convert focal length to pixels
f_pixels = f_mm * (render_width_px / sensor_width_mm)
baseline_m = 0.04

# ---- Process ----
process_depth_exr_disparity(left_exr, left_output, f_pixels, baseline_m)
# process_depth_exr_disparity(right_exr, right_output, f_pixels, baseline_m)

print("Done! Disparity visualizations saved as:", left_output)















# # Generated to iterate over images in folder
# import os
# import re
# import glob
# import numpy as np
# import OpenEXR
# import Imath
# import matplotlib.pyplot as plt
# from PIL import Image


# def read_exr_channel(exr_path, channel='R'):
#     """Read a single channel from an EXR file as float32 numpy array."""
#     exr_file = OpenEXR.InputFile(exr_path)
#     header = exr_file.header()
#     dw = header['dataWindow']

#     width = dw.max.x - dw.min.x + 1
#     height = dw.max.y - dw.min.y + 1

#     pt = Imath.PixelType(Imath.PixelType.FLOAT)
#     ch_str = exr_file.channel(channel, pt)

#     ch = np.frombuffer(ch_str, dtype=np.float32)
#     ch.shape = (height, width)

#     return ch


# def process_depth_exr_disparity(input_path, output_path, f_pixels, baseline_m, max_depth=1.95):
#     """Convert depth EXR to disparity visualization."""

#     depth = read_exr_channel(input_path, channel='R')

#     depth = np.nan_to_num(depth, nan=np.inf, posinf=np.inf, neginf=np.inf)

#     mask = depth > max_depth

#     depth[depth <= 0] = 1e-6

#     disparity = (f_pixels * baseline_m) / depth

#     disparity[mask] = np.nan

#     cmap = plt.cm.Spectral_r.copy()
#     cmap.set_bad(color='black')

#     plt.imsave(output_path, disparity, cmap=cmap,
#                vmin=0, vmax=np.nanmax(disparity))


# # Camera constants
# sensor_width_mm = 6.7
# render_width_px = 640

# # Folder root
# script_dir = os.path.dirname(os.path.abspath(__file__))
# results_root = os.path.join(script_dir, "disparity_results")
# pdf_output_root = os.path.join(script_dir, "addit_data_samples_new")
# os.makedirs(pdf_output_root, exist_ok=True)


# # Iterate folders
# for folder in os.listdir(results_root):

#     folder_path = os.path.join(results_root, folder)

#     if not os.path.isdir(folder_path):
#         continue

#     print("Processing:", folder)

#     # -------- Extract parameters from folder name --------

#     f_match = re.search(r'f(\d+)', folder)
#     i_match = re.search(r'i(\d+)', folder)

#     if not f_match or not i_match:
#         print("Skipping (cannot parse params)")
#         continue

#     f_code = f_match.group(1)
#     i_code = i_match.group(1)

#     # f25 -> 2.5mm, f15 -> 1.5mm
#     f_mm = float(f_code) / 10

#     # i004 -> 0.04m
#     baseline_m = float(i_code) / 100

#     # Convert focal length to pixels
#     f_pixels = f_mm * (render_width_px / sensor_width_mm)

#     # -------- Find left EXR --------

#     exr_files = [f for f in os.listdir(folder_path) if f.endswith("_L.exr")]

#     if len(exr_files) == 0:
#         print("No left EXR found")
#         continue

#     left_exr = os.path.join(folder_path, exr_files[0])

#     output_path = os.path.join(folder_path, "left_disparity_vis.png")

#     process_depth_exr_disparity(left_exr, output_path, f_pixels, baseline_m)

#     print("Saved:", output_path)

#     # -------- Convert images to PDF --------
#     folder_name = os.path.basename(folder_path)
#     pdf_output_folder = os.path.join(pdf_output_root, folder_name)
#     os.makedirs(pdf_output_folder, exist_ok=True)

#     patterns = ["*_L.jpg", "*_R.jpg", "*_disparity_vis.png"]
#     files_to_convert = []
#     for pattern in patterns:
#         files_to_convert.extend(glob.glob(os.path.join(folder_path, pattern)))

#     for input_path in files_to_convert:
#         filename = os.path.basename(input_path)
#         output_filename = os.path.splitext(filename)[0] + ".pdf"
#         output_path = os.path.join(pdf_output_folder, output_filename)

#         img = Image.open(input_path)
#         if img.mode != "RGB":
#             img = img.convert("RGB")

#         img.save(output_path)
#         print(f"Saved PDF: {output_path}")

# print("All disparity images and PDFs generated.")

