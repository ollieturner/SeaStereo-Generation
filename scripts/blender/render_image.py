# TO VERIFY 

# Render a single Blender image 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 


# --- RUN INSTRUCTIONS ---
# Note the file paths are still hardcoded

# blender -b /home/otur3695/Documents/Blender/blender_files/current_underwater_scene.blend \
#         --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/render_image.py

# blender -b /home/otur3695/Documents/Blender/blender_files/underwater_tutorials/underwater_scene.blend \
#         --python /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/scripts/blender/render_image.py

# From inside folder with script: 
# blender -b /home/otur3695/Documents/Blender/<file_name>.blend --python render_image.py

# RUN THIS ONE: 
# blender -b /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender/underwater_scene.blend \
#         --python /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/scripts/blender/render_image.py



# --- TO DO ---
# - Make run command smoother
# --> Build in files to run, not as input arguments
# - customise output file path - make a prompt? (can iterate)


import bpy
import os

# Output path
output_path = os.path.expanduser("/home/otur3695/Documents/Blender/results/blender_output/delete_global/")
# output_path = os.path.expanduser("/home/otur3695/Documents/Blender/automate_test/blender_render_background.png")

# Set render output
bpy.context.scene.render.filepath = output_path

# Render still image
bpy.ops.render.render(write_still=True)

print(f"Render saved to {output_path}")
