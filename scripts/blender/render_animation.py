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


# Import libraries
import bpy
import os

# Define scene
scene = bpy.context.scene

# Define render output path (already in .blend file but for backup, also can override if desired)
output_path = os.path.expanduser("results/blender_output/temp/")

# Set render output
scene.render.filepath = output_path

# Set frame range (limit for demos)
scene.frame_start = 1
scene.frame_end = 1

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


