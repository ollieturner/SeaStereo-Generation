import OpenEXR
import Imath
import numpy as np
import matplotlib.pyplot as plt
import os

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

# 35
def process_depth_exr_disparity(input_path, output_path, f_pixels, baseline_m, max_depth=100.0, epsilon=1e-6):
    """Convert depth EXR to disparity visualization with gamma scaling and Spectral_r colormap."""
    # Read depth
    depth = read_exr_channel(input_path, channel='R')
    depth = np.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0)

    # # Clip all values above max_depth
    # depth_clip = np.clip(depth, 0, max_depth)
    depth_clip = depth

    # Convert depth to disparity using camera parameters
    disparity = (f_pixels * baseline_m) / (depth_clip + epsilon)

    # Normalize disparity to [0,1] for visualization
    vmin = disparity.min()
    vmax = np.percentile(disparity, 100)  # can use percentile if you want to clip outliers
    disparity_clip = np.clip(disparity, vmin, vmax)

    if vmax > vmin:
        disp_norm = (disparity_clip - vmin) / (vmax - vmin)
        disp_vis = np.sqrt(disp_norm)  # gamma = 0.5
    else:
        disp_vis = np.zeros_like(disparity_clip)

    # Save image with Spectral_r colormap (red=close, blue=far)
    plt.imsave(output_path, disp_vis, cmap='Spectral_r')

# ---- Paths ----
script_dir = os.path.dirname(os.path.abspath(__file__))

# Auto-detect left/right EXR files in the folder
left_exr = None
right_exr = None
for f in os.listdir(script_dir):
    if f.endswith('_L.exr'):
        left_exr = os.path.join(script_dir, f)
    elif f.endswith('_R.exr'):
        right_exr = os.path.join(script_dir, f)

if left_exr is None or right_exr is None:
    raise FileNotFoundError("Could not find left or right EXR files in the script directory.")

left_output = os.path.join(script_dir, "left_disparity_vis.png")
right_output = os.path.join(script_dir, "right_disparity_vis.png")

# ---- Camera parameters from Blender ----
# f_pixels = 700      # focal length in pixels (convert from mm if needed)
# baseline_m = 0.065  # distance between cameras in meters (Blender interocular distance)


# # ---- Blender camera parameters ----
# f_mm = 35.0                 # Blender focal length in mm
# sensor_width_mm = 32.0      # Blender camera sensor width in mm
# render_width_px = 1920       # image width in pixels
# baseline_m = 0.065           # interocular distance (baseline) in meters


# ---- Blender camera parameters ----
f_mm = 1.5                 # Blender focal length in mm
sensor_width_mm = 6.7      # Blender camera sensor width in mm
render_width_px = 640       # image width in pixels

# Convert focal length to pixels
f_pixels = f_mm * (render_width_px / sensor_width_mm)
baseline_m = 0.04 # 0.08 


# ---- Process ----
process_depth_exr_disparity(left_exr, left_output, f_pixels, baseline_m)
process_depth_exr_disparity(right_exr, right_output, f_pixels, baseline_m)

print("Done! Disparity visualizations saved as:", left_output, right_output)























# # OLD

# import OpenEXR
# import Imath
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# def read_exr_channel(exr_path, channel='R'):
#     """Read a single channel from an EXR file as a float32 numpy array."""
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

# # WORKING
# # def process_depth_exr(input_path, output_path):
# #     depth = read_exr_channel(input_path, channel='R')
# #     depth = np.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0)

# #     # Clip the farthest 5% of values for visualization
# #     vmin = depth.min()
# #     vmax = np.percentile(depth, 58.7) # 80 ) # 95)  # farthest 5% clipped

# #     depth_clip = np.clip(depth, vmin, vmax)

# #     # Normalize and apply gamma scaling
# #     if vmax > vmin:
# #         depth_norm = (depth_clip - vmin) / (vmax - vmin)
# #         depth_vis = np.sqrt(depth_norm)  # gamma=0.5
# #     else:
# #         depth_vis = np.zeros_like(depth_clip)

# #     plt.imsave(output_path, depth_vis, cmap='jet')

# # 100m, 35
# def process_depth_exr(input_path, output_path, max_depth=35.0):
#     depth = read_exr_channel(input_path, channel='R')
#     depth = np.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0)

#     # Clip all values above max_depth
#     depth_clip = np.clip(depth, 0, max_depth)

#     # Normalize 0 → max_depth
#     depth_norm = depth_clip / max_depth

#     # Apply gamma scaling to enhance mid-range depth
#     depth_vis = np.sqrt(depth_norm)  # gamma = 0.5

#     plt.imsave(output_path, depth_vis, cmap='jet')


# # ---- Paths ----
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Auto-detect left/right EXR files in the folder
# left_exr = None
# right_exr = None
# for f in os.listdir(script_dir):
#     if f.endswith('_L.exr'):
#         left_exr = os.path.join(script_dir, f)
#     elif f.endswith('_R.exr'):
#         right_exr = os.path.join(script_dir, f)

# if left_exr is None or right_exr is None:
#     raise FileNotFoundError("Could not find left or right EXR files in the script directory.")

# left_output = os.path.join(script_dir, "left_depth_vis.png")
# right_output = os.path.join(script_dir, "right_depth_vis.png")

# # ---- Process ----
# process_depth_exr(left_exr, left_output)
# process_depth_exr(right_exr, right_output)

# print("Done! Visualizations saved as:", left_output, right_output)





# # import cv2
# # import numpy as np
# # import matplotlib.pyplot as plt

# # def process_depth_exr(input_path, output_path):
# #     # Load EXR with full float precision
# #     depth = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

# #     if depth is None:
# #         raise ValueError(f"Could not load file: {input_path}")

# #     # If multi-channel, take first channel
# #     if len(depth.shape) == 3:
# #         depth = depth[:, :, 0]

# #     depth = depth.astype(np.float32)

# #     # Replace NaN/Inf
# #     depth = np.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0)

# #     # Clip extreme values (robust visualization)
# #     vmin = np.percentile(depth, 1)
# #     vmax = np.percentile(depth, 99)

# #     if vmax > vmin:
# #         depth = np.clip(depth, vmin, vmax)
# #         depth = (depth - vmin) / (vmax - vmin)
# #     else:
# #         depth = np.zeros_like(depth)

# #     # Save image (red-blue colormap)
# #     plt.imsave(output_path, depth, cmap='seismic')

# # # ---- Paths ----
# # # left_exr_path = 'raw_depth0001_L.exr'
# # # right_exr_path = 'raw_depth0001_R.exr'

# # left_output_path = "left_depth_vis.png"
# # right_output_path = "right_depth_vis.png"

# # import os
# # script_dir = os.path.dirname(os.path.abspath(__file__))
# # # print(os.listdir(script_dir))

# # left_exr_path = os.path.join(script_dir, "raw_depth0001_L.exr")
# # right_exr_path = os.path.join(script_dir, "raw_depth0001_R.exr")

# # # ---- Process independently ----
# # process_depth_exr(left_exr_path, left_output_path)
# # process_depth_exr(right_exr_path, right_output_path)