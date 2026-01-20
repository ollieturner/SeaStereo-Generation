# TO VERIFY 

# Render a series images for one animation 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 
# Saves renders into folder: /home/otur3695/Documents/Blender/results/blender_output/


# --- RUN INSTRUCTIONS ---
# Note the file paths are still hardcoded

# From anywhere:
# blender -b /home/otur3695/Documents/Blender/blender_files/current_underwater_scene.blend \
#         --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/render_animation.py

# From inside folder with script: 
# blender -b /home/otur3695/Documents/Blender/<file_name>.blend --python render_animation.py


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

# Save the global renders to a folder to then delete at the end - no option to disable this yet in Blender (see 'Known Issues in README)
# Other renders (raw image, raw depth) have their output path encoded in Compositing tab in Blender
output_path = os.path.expanduser("/home/otur3695/Documents/Blender/results/blender_output/delete_global/")

# Set render output
scene.render.filepath = output_path

# Set frame range (limit for demos)
scene.frame_start = 1
scene.frame_end = 240

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


