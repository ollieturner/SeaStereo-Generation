# Render a series images for one animation 
# No iterating over configurations/changing settings - renders scene as it is in Blender file 
# Saves renders into folder: /home/otur3695/Documents/Blender/results/blender_output/


# --- RUN INSTRUCTIONS ---
# From root of repo
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/render_animation.py

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
scene.render.resolution_x = 1920 # 40 # 1920 # 854
scene.render.resolution_y = 1080 # 480 # 1080 # 480
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
scene.frame_end = 1

# Render animation
bpy.ops.render.render(animation=True)

print("Animation render complete")


