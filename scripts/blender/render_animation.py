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


