# Testing out improvements/different setups for rendering animations
# Render a series Blender images for animation
# Saves renders into folder: /home/otur3695/Documents/Blender/results/blender_output/


# --- RUN INSTRUCTIONS ---
# Note the file paths are still hardcoded

# From anywhere:
# blender -b /home/otur3695/Documents/Blender/blender_files/current_underwater_scene.blend \
#         --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/test_render_animation.py

# From inside folder with script: 
# blender -b /home/otur3695/Documents/Blender/<file_name>.blend --python test_render_animation.py


# --- TASKS ---
# Rendering images into output folder, then moving them somewhere else
# Rendering each camera configuration and saving each into their own folder


# --- TO DO ---
# Make run command smoother
# --> Build in files to run, not as input arguments
# Iterate over configurations (create folders, unique naming)
# --> Do customisations of configurations in here or manually in blender?
# Customise output file path - (can iterate over folders)
# Make it create the save folder
# Change to save into results folder here and in blender, then move files to desired position 


# --- RENDERING THEN MOVING FILES ---

# Import libraries
import bpy
import os
import shutil
from glob import glob

# Define scene
scene = bpy.context.scene

# TODO Update with delete_global/ folder 
# The original Blender output folder (set for global render, others are encoded in Blender Compositing tab)
blender_output = "/home/otur3695/Documents/Blender/results/blender_output/"

# Desired location folder
custom_folder = "/home/otur3695/Documents/Blender/results/test_rendering/"
os.makedirs(custom_folder, exist_ok=True)

# Set frame range
scene.frame_start = 1
scene.frame_end = 2

# Render animation
bpy.ops.render.render(animation=True)

print("Render complete, now moving files...")

# Move all files from Blender output to custom folder
for file_path in glob(os.path.join(blender_output, "*")):
    # construct destination
    dest = os.path.join(custom_folder, os.path.basename(file_path))
    shutil.move(file_path, dest)

print("Files moved to custom folder")




# # --- SELECTING AND RENDERING MULTIPLE CAMERAS ---

# NEW VERSION TO TEST:
# import bpy
# import os

# scene = bpy.context.scene

# camera_collection_name = "Cameras"
# camera_collection = bpy.data.collections.get(camera_collection_name)
# if not camera_collection:
#     raise RuntimeError(f"Collection '{camera_collection_name}' not found")

# output_base = "/home/otur3695/Documents/Blender/results/blender_output/"

# scene.frame_start = 1
# scene.frame_end = 1

# scene.use_nodes = True
# tree = scene.node_tree

# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     print(f"Rendering animation from camera: {cam_obj.name}")

#     scene.camera = cam_obj

#     cam_output_path = os.path.join(output_base, cam_obj.name)
#     os.makedirs(cam_output_path, exist_ok=True)

#     # Render Result output
#     scene.render.filepath = cam_output_path + "/"

#     # 🔑 Compositor File Output nodes
#     for node in tree.nodes:
#         if node.type == 'OUTPUT_FILE':
#             node.base_path = cam_output_path

#     bpy.ops.render.render(animation=True)

# print("All camera animations complete")





# # not saving renders into correct folders, puts them in blender_output not in their respective camera folders
# # but does do it for the inverted normalised depth 

# import bpy
# import os

# scene = bpy.context.scene

# # Collection that contains your cameras
# camera_collection_name = "Cameras"
# camera_collection = bpy.data.collections.get(camera_collection_name)
# if not camera_collection:
#     raise RuntimeError(f"Collection '{camera_collection_name}' not found")

# # Base output folder
# output_base = os.path.expanduser("/home/otur3695/Documents/Blender/results/blender_output/")

# # Frame range
# scene.frame_start = 1
# scene.frame_end = 1

# # Loop through cameras in the collection
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     print(f"Rendering animation from camera: {cam_obj.name}")

#     # Set this camera as the active scene camera
#     scene.camera = cam_obj

#     # Create camera-specific output folder
#     cam_output_path = os.path.join(output_base, cam_obj.name)
#     os.makedirs(cam_output_path, exist_ok=True)
#     scene.render.filepath = cam_output_path + "/"  # Blender needs a trailing slash

#     # Render animation
#     bpy.ops.render.render(animation=True)

# print("All camera animations complete")
