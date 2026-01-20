# NOT A FOCUS SINCE NEED SERIES OF IMAGES

# Render a single blender image 
# Choose blender file when running 

# # Inside folder with script: 
# blender -b /home/otur3695/Documents/Blender/cookie_auto_tutorial.blend --python base_single_image.py

# # From somewhere else:
# blender -b /home/otur3695/Documents/Blender/cookie_auto_tutorial.blend \
#         --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/base_single_image.py

# To do:
# - Make run command smoother
# --> Build in files to run, not as input arguments
# - customise output file path - make a prompt? (can iterate)

import bpy
import os

# Output path
output_path = os.path.expanduser("/home/otur3695/Documents/Blender/automate_test/blender_render_background.png")

# Set render output
bpy.context.scene.render.filepath = output_path

# Render still image
bpy.ops.render.render(write_still=True)

print(f"Render saved to {output_path}")


# scene.render.engine = 'CYCLES'        # or 'BLENDER_EEVEE'
# scene.cycles.device = 'CPU'           # or 'GPU'
# scene.render.resolution_x = 1920
# scene.render.resolution_y = 1080
# scene.render.image_settings.file_format = 'PNG'

