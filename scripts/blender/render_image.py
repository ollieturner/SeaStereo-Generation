# Render a single Blender image 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 


# --- RUN INSTRUCTIONS ---
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/render_image.py


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
