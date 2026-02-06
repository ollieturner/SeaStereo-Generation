# Render a series images for one animation 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 
# Saves renders into folder: /results/blender_output/


# --- RUN INSTRUCTIONS ---
# From root of repo
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/render_animation.py

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
scene.frame_end = 30

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


