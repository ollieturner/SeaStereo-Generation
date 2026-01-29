
# Make it just do one frame each 

# WRITE PLAN FIRST

# Make option at start to select all the options 
# Check against current render animation 


# blender -b /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender/underwater_scene.blend \
#         --python /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/scripts/blender/generate_sample_dataset.py

# blender -b blender/underwater_scene.blend --python scripts/blender/generate_dataset.py


# Render into normal folder then move files 
# Had trouble trying to change where the compositing nodes saved



# TO DO: 
# Update paths so it is relative 
# Delete the delete_global
# Use spotlights for clear and murky conditions 
# Random number of objects between 3 and 5 
# Account for collections in Everyday Objects 
# Add a render tag? Just do that for sample, and a how many frames tag 



# CAMERA × WATER × Z × RANDOM ARRANGEMENTS + LIGHTS + OBJECTS

# Import libraries 
import bpy
import os
import shutil
import random
import math

RENDER = False

# Define base export save path
BASE_SAVE_PATH = "results/blender_output/"

# Water conditions (name, label)
WATER_CONDITIONS = [
    ("Jerlov",     "Jerlov I"),
    ("Jerlov.001", "Jerlov IA"),
    ("Jerlov.005", "Jerlov IB"),        # Clearest ones ^ 
    ("Jerlov.004", "Jerlov II"),
    ("Jerlov.003", "Jerlov IC"),        # Slightly murky but still clear. Use Clear camera spotlight ^ 
    ("Jerlov.002", "Jerlov III"),       # Use Murky camera spotlight for this and below 
    ("Jerlov.007", "Jerlov 5C"),
    ("Jerlov.006", "Jerlov 3C")
    # ("Jerlov.008", "Jerlov 7C"),      # Too murky, can't see anything 
    # ("Jerlov.009", "Jerlov 9C")
]
# Define water clarity type for the lights 
# True = clear, False = murky
CLEAR_WATER_FRAMES = ["Jerlov", "Jerlov.001", "Jerlov.005", "Jerlov.004", "Jerlov.003"]
MURKY_WATER_FRAMES = ["Jerlov.002", "Jerlov.007", "Jerlov.006"]

# Z offsets for Ocean Volume
Z_OFFSETS = [-20, -10, -5]

# Number of random arrangements per camera × water × Z
NUM_RANDOM_ARRANGEMENTS = 3
MIN_OBJECTS, MAX_OBJECTS = 3, 5

# 3x3 grid bounds for Everyday Objects in foreground
GRID_MIN = -1.5
GRID_MAX = 1.5

# Get Ocean Volume and its volume coefficients for the water conditions
MAT_NAME = "Ocean Volume"
mat = bpy.data.materials.get(MAT_NAME)
if not mat:
    raise RuntimeError(f"Material '{MAT_NAME}' not found")

nodes = mat.node_tree.nodes
links = mat.node_tree.links
vol = nodes.get("Volume Coefficients")
if not vol:
    raise RuntimeError("Volume Coefficients node not found")


# Define the scene
scene = bpy.context.scene

# Get collections
camera_collection = bpy.data.collections.get("Cameras")
light_collection = bpy.data.collections.get("Camera Lights")
ocean_collection = bpy.data.collections.get("Ocean")
objects_collection = bpy.data.collections.get("Everyday Objects")

if not camera_collection:
    raise RuntimeError("Camera collection not found")
if not light_collection:
    raise RuntimeError("Lights collection not found")
if not ocean_collection:
    raise RuntimeError("Ocean collection not found")
if not objects_collection:
    raise RuntimeError("Everyday Objects collection not found")

ocean_obj = ocean_collection.objects.get("Ocean Volume")
if not ocean_obj:
    raise RuntimeError("Ocean Volume object not found in 'Ocean' collection")


# Extract all the everyday objects from their sub-collections
all_objects = []
for subcol in objects_collection.children:
    all_objects.extend(subcol.objects)

if len(all_objects) < MAX_OBJECTS:
    raise RuntimeError("Not enough objects to sample from")

# -----------------------------
# TEMP OUTPUT
# -----------------------------
temp_output = os.path.join(BASE_SAVE_PATH, "temp")
os.makedirs(temp_output, exist_ok=True)

scene.frame_start = 1
scene.frame_end = 1

# Compositor node tree
tree_name = "Render Output"
tree = bpy.data.node_groups.get(tree_name)
if not tree or tree.bl_idname != "CompositorNodeTree":
    raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

# -----------------------------
# MAIN LOOP: Cameras × Water × Z × Random Arrangement
# -----------------------------
for cam_obj in camera_collection.objects:
    if cam_obj.type != 'CAMERA':
        continue

    scene.camera = cam_obj
    print(f"\n=== Camera: {cam_obj.name} ===")

    for frame_name, label in WATER_CONDITIONS:
        print(f"\n--- Water condition: {label} ({frame_name}) ---")


        ## SELECT CAMERA SPOTLIGHT IF CLEAR OR MURKY 
        # Determine water clarity
        if frame_name in CLEAR_WATER_FRAMES:
            water_type = "Clear"
        else:
            water_type = "Murky"

        # Disable all lights first
        for l in light_collection.objects:
            l.hide_render = True

        # Construct spotlight name
        base_spot_name = cam_obj.name.replace("Camera", "Spot")
        spotlight_name = f"{water_type} {base_spot_name}"
        spotlight = light_collection.objects.get(spotlight_name)

        # Enable correct spotlight
        if spotlight:
            spotlight.hide_render = False
            print(f"Enabled light: {spotlight.name}")
        else:
            print(f"Warning: no matching {water_type} spotlight found for {cam_obj.name}")


        # -----------------------------
        # Switch water condition
        # -----------------------------
        frame = nodes.get(frame_name)
        if not frame or frame.type != 'FRAME':
            print(f"Warning: frame '{frame_name}' not found or wrong type")
            continue

        # Remove existing links
        for inp in vol.inputs:
            for lnk in list(inp.links):
                links.remove(lnk)

        vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
        if len(vec_nodes) != 2:
            print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")
            continue

        abs_node, scat_node = vec_nodes
        try:
            links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
            links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])
        except Exception as e:
            print(f"Failed to connect nodes for {frame_name}: {e}")
            continue

        print(f"Switched water condition to {label}")

        # -----------------------------
        # LOOP OVER Z OFFSETS
        # -----------------------------
        for z in Z_OFFSETS:
            ocean_obj.location.z = z
            print(f"Set Ocean Volume Z to: {z} m")

            # -----------------------------
            # LOOP OVER RANDOM ARRANGEMENTS
            # -----------------------------
            for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
                print(f"Random arrangement {arr_idx}")

                # --- Initially disable all objects for render ---
                for obj in all_objects:
                    obj.hide_render = True

                # --- randomly select objects ---
                NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)  # 3-5 objects
                selected_objects = random.sample(all_objects, NUM_OBJECTS)

                # Randomize objects positions within foreground grid, keep original Z
                for obj in selected_objects:
                    obj.hide_render = False
                    obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
                    obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
                    rot = random.uniform(0, 2*math.pi)
                    obj.rotation_euler.z = rot
                

                if RENDER:
                    # Render everything to the temp folder
                    scene.render.filepath = temp_output + "/"
                    bpy.ops.render.render(animation=True)

                    # Move outputs to Camera/Water/Z/Arrangement folder
                    cam_water_z_folder = os.path.join(
                        BASE_SAVE_PATH,
                        cam_obj.name,
                        frame_name,
                        f"Z_{z}m",
                        f"Arrangement_{arr_idx}"
                    )
                    os.makedirs(cam_water_z_folder, exist_ok=True)

                    for item in os.listdir(temp_output):
                        src = os.path.join(temp_output, item)
                        dst = os.path.join(cam_water_z_folder, item)
                        if os.path.exists(dst):
                            if os.path.isdir(dst):
                                shutil.rmtree(dst)
                            else:
                                os.remove(dst)
                        shutil.move(src, dst)

                    # Recreate temp folder for next render
                    os.makedirs(temp_output, exist_ok=True)

                    print(f"Saved outputs to: {cam_water_z_folder}")


print("\nAll camera x water x Z x random arrangement renders complete.")


























# ## ORIGINAL

# # CAMERA × WATER × Z × RANDOM ARRANGEMENTS + LIGHTS + OBJECTS
# import bpy
# import os
# import shutil
# import random

# # -----------------------------
# # CONFIG
# # -----------------------------
# MAT_NAME = "Ocean Volume"
# BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results/blender_output/"

# # Water conditions (name, label)
# WATER_CONDITIONS = [
#     ("Jerlov",     "Jerlov I"),     
#     # ("Jerlov.004", "Jerlov II"),
#     # ("Jerlov.002", "Jerlov III"),
#     ("Jerlov.001", "Jerlov IA"),
#     ("Jerlov.005", "Jerlov IB")
# ]

# # Z offsets for Ocean Volume
# Z_OFFSETS = [-20, -10, -5]

# # Number of random arrangements per camera × water × Z
# NUM_RANDOM_ARRANGEMENTS = 3

# # 2x2 grid bounds for objects
# GRID_MIN = -1.0
# GRID_MAX = 1.0

# # -----------------------------
# # GET MATERIAL (Ocean Volume)
# # -----------------------------
# mat = bpy.data.materials.get(MAT_NAME)
# if not mat:
#     raise RuntimeError(f"Material '{MAT_NAME}' not found")

# nodes = mat.node_tree.nodes
# links = mat.node_tree.links
# vol = nodes.get("Volume Coefficients")
# if not vol:
#     raise RuntimeError("Volume Coefficients node not found")

# # -----------------------------
# # COLLECTIONS
# # -----------------------------
# scene = bpy.context.scene
# camera_collection = bpy.data.collections.get("Cameras")
# light_collection = bpy.data.collections.get("Camera Lights")
# ocean_collection = bpy.data.collections.get("Ocean")
# objects_collection = bpy.data.collections.get("Everyday Objects")

# if not camera_collection:
#     raise RuntimeError("Camera collection not found")
# if not light_collection:
#     raise RuntimeError("Lights collection not found")
# if not ocean_collection:
#     raise RuntimeError("Ocean collection not found")
# if not objects_collection:
#     raise RuntimeError("Everyday Objects collection not found")

# ocean_obj = ocean_collection.objects.get("Ocean Volume")
# if not ocean_obj:
#     raise RuntimeError("Ocean Volume object not found in 'Ocean' collection")

# # -----------------------------
# # TEMP OUTPUT
# # -----------------------------
# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# scene.frame_start = 1
# scene.frame_end = 30 # CHANGE TO 2030

# # Compositor node tree
# tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

# # -----------------------------
# # MAIN LOOP: Cameras × Water × Z × Random Arrangement
# # -----------------------------
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"\n=== Camera: {cam_obj.name} ===")

#     # Disable all camera lights first
#     for l in light_collection.objects:
#         l.hide_render = True

#     # Enable matching spotlight
#     spotlight_name = cam_obj.name.replace("Camera", "Spot")
#     spotlight = light_collection.objects.get(spotlight_name)
#     if spotlight:
#         spotlight.hide_render = False
#         print(f"Enabled light: {spotlight.name}")
#     else:
#         print(f"Warning: no matching spotlight found for {cam_obj.name}")

#     for frame_name, label in WATER_CONDITIONS:
#         print(f"\n--- Water condition: {label} ({frame_name}) ---")

#         # -----------------------------
#         # Switch water condition
#         # -----------------------------
#         frame = nodes.get(frame_name)
#         if not frame or frame.type != 'FRAME':
#             print(f"Warning: frame '{frame_name}' not found or wrong type")
#             continue

#         # Remove existing links
#         for inp in vol.inputs:
#             for lnk in list(inp.links):
#                 links.remove(lnk)

#         vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
#         if len(vec_nodes) != 2:
#             print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")
#             continue

#         abs_node, scat_node = vec_nodes
#         try:
#             links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
#             links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])
#         except Exception as e:
#             print(f"Failed to connect nodes for {frame_name}: {e}")
#             continue

#         print(f"Switched water condition to {label}")

#         # -----------------------------
#         # LOOP OVER Z OFFSETS
#         # -----------------------------
#         for z in Z_OFFSETS:
#             ocean_obj.location.z = z
#             print(f"Set Ocean Volume Z to: {z} m")

#             # -----------------------------
#             # LOOP OVER RANDOM ARRANGEMENTS
#             # -----------------------------
#             for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
#                 print(f"Random arrangement {arr_idx}")

#                 # Randomize objects positions within 2x2 grid, keep original Z
#                 for obj in objects_collection.objects:
#                     obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
#                     obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
#                     # Z stays the same
                
#                 # TODO Make sure not clashing based on bounding box min/maxes

#                 # Render everything to the temp folder
#                 render_temp = os.path.join(temp_output, "delete_global")
#                 os.makedirs(render_temp, exist_ok=True)
#                 scene.render.filepath = render_temp + "/"
#                 bpy.ops.render.render(animation=True)

#                 # -----------------------------
#                 # DELETE ONLY delete_global FOLDER
#                 # -----------------------------
#                 if os.path.exists(render_temp):
#                     shutil.rmtree(render_temp)
#                     print(f"Deleted temporary global render folder: {render_temp}")

#                 # Move outputs to Camera/Water/Z/Arrangement folder
#                 cam_water_z_folder = os.path.join(
#                     BASE_SAVE_PATH,
#                     cam_obj.name,
#                     frame_name,
#                     f"Z_{z}m",
#                     f"Arrangement_{arr_idx}"
#                 )
#                 os.makedirs(cam_water_z_folder, exist_ok=True)

#                 for item in os.listdir(temp_output):
#                     src = os.path.join(temp_output, item)
#                     dst = os.path.join(cam_water_z_folder, item)
#                     if os.path.exists(dst):
#                         if os.path.isdir(dst):
#                             shutil.rmtree(dst)
#                         else:
#                             os.remove(dst)
#                     shutil.move(src, dst)

#                 # Recreate temp folder for next render
#                 os.makedirs(temp_output, exist_ok=True)

#                 print(f"Saved outputs to: {cam_water_z_folder}")

#     # Disable spotlight after camera is done
#     if spotlight:
#         spotlight.hide_render = True

# print("\nAll camera × water × Z × random arrangement renders complete.")
