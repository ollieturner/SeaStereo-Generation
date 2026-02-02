# Render a series images for one animation 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 
# Saves renders into folder: /home/otur3695/Documents/Blender/results/blender_output/


# --- RUN INSTRUCTIONS ---
# Note the file paths are still hardcoded

# From anywhere:
# blender -b /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender/underwater_scene.blend \
#         --python /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/scripts/blender/render_animation.py

# From inside folder with script: 
# blender -b /home/otur3695/Documents/Blender/underwater_scene.blend --python render_animation.py

# blender -b blender/underwater_scene.blend --python scripts/blender/render_animation.py


# --- TO DO ---
# Make run command smoother
# --> Build in files to run, not as input arguments
# Customise output file path - (can iterate over folders)
# Make it create the save folder, if it does exist already
# Change to save into results folder here and in blender, then move files to desired position 
# Delete the global render 
# ** See test_render_animation.py for current progress on these improvements


# Add in changing resolution 

# Import libraries
import bpy
import os

# Define scene
scene = bpy.context.scene


# ----------------------------
# Resolution info (print)
# ----------------------------
res_x = scene.render.resolution_x
res_y = scene.render.resolution_y
res_pct = scene.render.resolution_percentage

print(f"Render resolution: {res_x} x {res_y}")
print(f"Resolution percentage: {res_pct}%")


# ----------------------------
# Resolution override (optional)
# Uncomment to force resolution
# ----------------------------
scene.render.resolution_x = 640 # 1920 # 854
scene.render.resolution_y = 480 # 1080 # 480
scene.render.resolution_percentage = 100

# DO 640 x 480

res_x = scene.render.resolution_x
res_y = scene.render.resolution_y
res_pct = scene.render.resolution_percentage

print(f"Render resolution: {res_x} x {res_y}")
print(f"Resolution percentage: {res_pct}%")


engine = scene.render.engine
print(f"Render engine: {engine}")


# Define render output path (already in .blend file but for backup, also can override if desired)
output_path = os.path.expanduser("results/blender_output/temp/")

# Set render output
scene.render.filepath = output_path

# Set frame range (limit for demos)
scene.frame_start = 1
scene.frame_end = 240

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


