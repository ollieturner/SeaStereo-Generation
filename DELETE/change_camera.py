# NOT PRIORITY 

# To enable and render each camera one-by-one, saving into their respective folders - RENDERING UNTESTED
import bpy
import os

# -----------------------------
# CONFIG
# -----------------------------
COLLECTION_NAME = "Cameras"
BASE_OUTPUT_PATH = REDO # "/home/otur3695/Documents/Blender/results/blender_anim/"
FRAME_START = 1
FRAME_END = 5

# -----------------------------
# GET CAMERA COLLECTION
# -----------------------------
cam_collection = bpy.data.collections.get(COLLECTION_NAME)
if not cam_collection:
    raise RuntimeError(f"Collection '{COLLECTION_NAME}' not found")

# Get all cameras in collection
cameras = [obj for obj in cam_collection.objects if obj.type == 'CAMERA']
if not cameras:
    raise RuntimeError(f"No cameras found in collection '{COLLECTION_NAME}'")

print(f"Found {len(cameras)} cameras:")
for c in cameras:
    print(" -", c.name)

scene = bpy.context.scene
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END

# -----------------------------
# LOOP OVER CAMERAS
# -----------------------------
for cam in cameras:
    print(f"\n=== Rendering from camera: {cam.name} ===")
    
    # Set active camera
    scene.camera = cam

    print("Checking current render camera:", bpy.context.scene.camera.name)

    # Create camera-specific output folder
    cam_output_path = os.path.join(BASE_OUTPUT_PATH, cam.name)
    os.makedirs(cam_output_path, exist_ok=True)
    scene.render.filepath = os.path.join(cam_output_path, "")
    
    # Render animation
    bpy.ops.render.render(animation=True)
    print(f"Animation saved to: {cam_output_path}")

print("\nAll cameras rendered successfully.")









# # To enable each camera and save new blender file with that active camera 
# # To test that its selecting cameras properly 
# import bpy
# import os

# # -----------------------------
# # CONFIG
# # -----------------------------
# COLLECTION_NAME = "Cameras"
# BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results_7_1/test_camera.blend"

# # -----------------------------
# # GET CAMERA COLLECTION
# # -----------------------------
# cam_collection = bpy.data.collections.get(COLLECTION_NAME)
# if not cam_collection:
#     raise RuntimeError(f"Collection '{COLLECTION_NAME}' not found")

# # Get all cameras in collection
# cameras = [obj for obj in cam_collection.objects if obj.type == 'CAMERA']
# if not cameras:
#     raise RuntimeError(f"No cameras found in collection '{COLLECTION_NAME}'")

# print(f"Found {len(cameras)} cameras:")
# for c in cameras:
#     print(" -", c.name)

# scene = bpy.context.scene

# # -----------------------------
# # LOOP OVER CAMERAS AND SAVE
# # -----------------------------
# for cam in cameras:
#     print(f"\n=== Switching active camera to: {cam.name} ===")
    
#     # Set active camera
#     scene.camera = cam

#     print("Current render camera:", bpy.context.scene.camera.name)

#     # # Optional: enable this camera in viewport and for render
#     # cam.hide_viewport = False  # show in 3D viewport
#     # cam.hide_render = False    # include in render
    
#     # Save file after switching
#     save_path = BASE_SAVE_PATH.replace(".blend", f"_{cam.name}.blend")
#     bpy.ops.wm.save_as_mainfile(filepath=save_path)
    
#     print(f"Saved Blender file to: {save_path}")

# print("\nCamera switching complete.")









# To check available cameras in Cameras collection
# Output:
# Cameras in collection 'Cameras':
# - Yiran Camera Setup
# - Ollie Camera Horizontal
# - Ollie Camera Vertical


# import bpy

# COLLECTION_NAME = "Cameras"

# # Get the collection
# cam_collection = bpy.data.collections.get(COLLECTION_NAME)
# if not cam_collection:
#     raise RuntimeError(f"Collection '{COLLECTION_NAME}' not found")

# print(f"Cameras in collection '{COLLECTION_NAME}':")
# for obj in cam_collection.objects:
#     if obj.type == 'CAMERA':
#         print(f"- {obj.name}")
