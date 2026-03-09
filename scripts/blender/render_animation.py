# # Import libraries
# import bpy
# import os
# import sys

# # --- Parse command-line argument for output path ---
# argv = sys.argv
# # Blender passes its own args first; after '--' are script args
# if "--" in argv:
#     argv = argv[argv.index("--") + 1:]  # args after --
# else:
#     argv = []

# if len(argv) > 0:
#     output_path = os.path.expanduser(argv[0])
# else:
#     output_path = os.path.expanduser("results/blender_output/temp/")  # default

# # Ensure the output directory exists
# os.makedirs(output_path, exist_ok=True)

# # Define scene
# scene = bpy.context.scene

# # Set render output
# scene.render.filepath = output_path

# # Set frame range
# scene.frame_start = 1
# scene.frame_end = 1  # 30

# # Render animation
# bpy.ops.render.render(animation=True)

# print(f"Animation render complete. Files saved to: {output_path}")

# # # Render a series images for one animation 
# # # No iterating over configurations/changing settings - renders scene as it is in Blender file 
# # # Saves renders into folder: /results/blender_output/


# --- RUN INSTRUCTIONS ---
# From root of repo
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/render_animation.py
# blender -b blender_scene/objects.blend --python scripts/blender/render_animation.py

# Import libraries
import bpy
import os

# Define scene
scene = bpy.context.scene

# Define render output path (already in .blend file but for backup, also can override if desired)
output_path = os.path.expanduser("results/blender_output/temp/")

# Set render output
scene.render.filepath = output_path

# Set frame range
scene.frame_start = 1
scene.frame_end = 1 # 30

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


