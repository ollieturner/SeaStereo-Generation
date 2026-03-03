
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/timing_analysis.py


print("Running timing script...\n")

import bpy
import os

# ----------------------------
# Output base path
# ----------------------------
base_output = os.path.expanduser("results/blender_output/temp/")

# Make sure folder exists
os.makedirs(base_output, exist_ok=True)

# ----------------------------
# Render plan
# Each entry is a dictionary of settings to override
# ----------------------------
render_plan = [
    # {"name": "Control"},  # default
    {"name": "Control_256_1_16", "samples": 256, "noise_threshold": 0.01, "max_bounces": 16},
    {"name": "Control_256_1_12", "samples": 256, "noise_threshold": 0.01, "max_bounces": 12},
    {"name": "Control_256_5_16", "samples": 256, "noise_threshold": 0.05, "max_bounces": 16},
    {"name": "Control_512_1_16", "samples": 512, "noise_threshold": 0.01, "max_bounces": 16},

]
#     {"name": "Control"},  # default
#     {"name": "Control_128", "samples": 128},
#     {"name": "Control_2048", "samples": 2048},
#     {"name": "Control_1024", "samples": 1024},
#     {"name": "Control_512", "samples": 512},
#     {"name": "Control_256", "samples": 256},
#     {"name": "Control_noise_0.05", "noise_threshold": 0.05},
#     {"name": "Control_noise_0.1", "noise_threshold": 0.1},
#     {"name": "Control_512_noise_0.05", "samples": 512, "noise_threshold": 0.05},
#     {"name": "Control_12_bounces", "max_bounces": 12},
# ]

# ----------------------------
# Loop through each render config
# ----------------------------
for config in render_plan:
    # Build output folder for this config
    config_output = os.path.join(base_output, config["name"])
    os.makedirs(config_output, exist_ok=True)
    
    scene = bpy.context.scene
    cycles = scene.cycles

    # ----------------------------
    # Override settings if specified
    # ----------------------------
    if "samples" in config:
        cycles.samples = config["samples"]
    
    if "noise_threshold" in config:
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = config["noise_threshold"]
    
    if "max_bounces" in config:
        scene.cycles.max_bounces = config["max_bounces"]
    
    # ----------------------------
    # Set the render filepath for this config
    # ----------------------------
    scene.render.filepath = os.path.join(config_output, "frame.png")
    
    # ----------------------------
    # Render
    # ----------------------------
    print(f"Rendering: {config['name']} -> {scene.render.filepath}")
    bpy.ops.render.render(write_still=True)
    
print("All renders complete!")