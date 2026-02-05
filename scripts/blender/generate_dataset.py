# Generate dataset
# See beginning of script for customisable features and render properties

# ------ RUN INSTRUCTIONS ------
# blender -b blender/underwater_scene.blend --python scripts/blender/generate_dataset.py


# TO DO 
# Make water lists one
# Fix depth offset
# Add in collision avoidance
# Make subfunctions
# Make two customisable sections 
# Add in changing camera properties 
# Size prediction at start 



# Import libraries 
# import bpy
import os
# import shutil
# import random
# import math
import sys

# Define the script directory to import helper functions 
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import helper_funcs_gen_dataset as func


## CUSTOMISE: RENDER PROPERTIES
# Set render flag 
RENDER = False
BASE_SAVE_PATH = "results/blender_output/"
frame_start = 1
frame_end = 1
res_x = 640
res_y = 480
res_pct = 100
tree_name = "Render Output"

scene, temp_output = func.apply_render_props(BASE_SAVE_PATH, frame_start, frame_end, res_x, res_y, res_pct, tree_name)


# # Define base export save path and temp output
# # BASE_SAVE_PATH = "results/blender_output/"
# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# # Define the scene
# scene = bpy.context.scene

# # Define the number of frames to render per configuration 
# scene.frame_start = frame_start # 1
# scene.frame_end = frame_end # 1 # 30

# # Define the resolution
# scene.render.resolution_x = res_x 
# scene.render.resolution_y = res_y 
# scene.render.resolution_percentage = res_pct

# # Set the compositor node tree
# # tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")




## CUSTOMISE: DATASET FEATURES
FOCAL_LENGTHS = [1.3, 2.0]
INTEROCULAR_DIST = [0.05, 0.07]

WATER_CONDITIONS = [
    ("Jerlov",     "Jerlov I",   "Clear"),
    ("Jerlov.001", "Jerlov IA",  "Clear"),
    ("Jerlov.005", "Jerlov IB",  "Clear"),
    ("Jerlov.004", "Jerlov II",  "Clear"),
    ("Jerlov.003", "Jerlov IC",  "Clear"),   
    ("Jerlov.002", "Jerlov III", "Murky"),
    ("Jerlov.007", "Jerlov 5C",  "Murky"),
    ("Jerlov.006", "Jerlov 3C",  "Murky"),
    # ("Jerlov.008", "Jerlov 7C"),      # Too murky, can't see anything 
    # ("Jerlov.009", "Jerlov 9C")
]

# Define depths for Ocean Volume
# Note: Offset of -25m in Blender = 0m depth e.g. -20m = 5m deep, -5m = 20m deep
CLEAR_Z_OFFSETS = [-20, -5]
MURKY_Z_OFFSETS = [-23]

# Number of random arrangements environment configuration
NUM_RANDOM_ARRANGEMENTS = 1 
MIN_OBJECTS, MAX_OBJECTS = 3, 5

# 3x3m grid bounds for Everyday Objects in foreground
GRID_MIN = -1.5
GRID_MAX = 1.5




# Get collections
camera_collection, light_collection, ocean_collection, objects_collection = func.get_collections()

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



func.print_render_msg(RENDER, frame_end, BASE_SAVE_PATH, res_x, res_y, res_pct)


# print("DATASET GENERATION FOR SIMULATED UNDERWATER SCENES\n")
# print("---RENDER PROPERTIES---")
# print(f"Rendering enabled: {RENDER}")
# print(f"Number of frames per configuration: {frame_end}")
# print(f"Renders will save into: {BASE_SAVE_PATH}")
# print(f"Render resolution: {res_x} x {res_y}")
# print(f"Resolution percentage: {res_pct}%\n")



func.print_dataset_msg(camera_collection, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX)


# print("---DATASET FEATURES---")

# # List available cameras
# print("Available cameras:")
# if len(camera_collection.objects) == 0:
#     print("  (No cameras found in 'Cameras' collection)")
# else:
#     for obj in camera_collection.objects:
#         if obj.type == 'CAMERA':
#             print(f"  - {obj.name}")


# print("Camera types: ")
# print(f"  Focal lengths: {FOCAL_LENGTHS[0]}mm, {FOCAL_LENGTHS[1]}mm")
# print(f"  Interocular distances: {INTEROCULAR_DIST[0]}mm, {INTEROCULAR_DIST[1]}mm")

# # Water conditions (human-readable only)
# print("Water conditions:")
# for _, label, _ in WATER_CONDITIONS:
#     print(f"  - {label}")

# # Depths (printed in real-world meters)
# print("Depths (real-world):")

# clear_depths = [func.blender_z_to_real_depth(z) for z in CLEAR_Z_OFFSETS]
# murky_depths = [func.blender_z_to_real_depth(z) for z in MURKY_Z_OFFSETS]

# print(f"  Clear water depths: {clear_depths} m")
# print(f"  Murky water depths: {murky_depths} m")

# # Object configuration
# print("Object placement:")
# print(f"  Objects per scene: {MIN_OBJECTS}–{MAX_OBJECTS}")
# print(f"  Random arrangements per configuration: {NUM_RANDOM_ARRANGEMENTS}")
# print(f"  Foreground grid: {GRID_MIN} m to {GRID_MAX} m (X/Y)")



func.get_confirmation()
# print("\nWith the current settings, this will take ~10 days, 2 hours to render")
# print("and use ~14.34 GB of storage.")
# print("Use Ctrl+C to cancel at any time.\n")


# # Confirmation prompt
# while True:
#     user_input = input("Proceed with dataset generation? (y/n): ").strip().lower()
#     if user_input in {"y", "yes"}:
#         print("Confirmed. Starting dataset generation\n")
#         print("Use Ctrl+C to cancel at anytime\n")
#         break
#     elif user_input in {"n", "no"}:
#         print("Dataset generation cancelled by user.")
#         raise SystemExit
#     else:
#         print("Please enter 'y' or 'n'.")




ocean_obj, nodes, links, vol = func.get_ocean_obj(ocean_collection)
# Get Ocean Volume and its volume coefficients for the water conditions
# ocean_obj = ocean_collection.objects.get("Ocean Volume")
# if not ocean_obj:
#     raise RuntimeError("Ocean Volume object not found in 'Ocean' collection")


# MAT_NAME = "Ocean Volume"
# mat = bpy.data.materials.get(MAT_NAME)
# if not mat:
#     raise RuntimeError(f"Material '{MAT_NAME}' not found")

# nodes = mat.node_tree.nodes
# links = mat.node_tree.links
# vol = nodes.get("Volume Coefficients")
# if not vol:
#     raise RuntimeError("Volume Coefficients node not found")




all_objects = func.get_everyday_obj(objects_collection, MAX_OBJECTS)
# Extract all the everyday objects from their sub-collections
# all_objects = []
# for subcol in objects_collection.children:
#     all_objects.extend(subcol.objects)

# if len(all_objects) < MAX_OBJECTS:
#     raise RuntimeError("Not enough objects to sample from")




# -----------------------------
# MAIN LOOP: Cameras × Water × Z × Random Arrangement
# -----------------------------
for cam_obj in camera_collection.objects:
    if cam_obj.type != 'CAMERA':
        continue

    scene.camera = cam_obj
    print(f"\n=== Camera: {cam_obj.name} ===")

    for frame_name, label, water_type in WATER_CONDITIONS:
        print(f"\n--- Water condition: {label} ({frame_name}) ---")

        func.enable_spotlight(light_collection, cam_obj, water_type)

        # # Disable all lights first
        # for l in light_collection.objects:
        #     l.hide_render = True

        # # Construct spotlight name
        # base_spot_name = cam_obj.name.replace("Camera", "Spot")
        # spotlight_name = f"{water_type} {base_spot_name}"
        # spotlight = light_collection.objects.get(spotlight_name)

        # # Enable correct spotlight
        # if spotlight:
        #     spotlight.hide_render = False
        #     print(f"Enabled light: {spotlight.name}")
        # else:
        #     print(f"Warning: no matching {water_type} spotlight found for {cam_obj.name}")


        func.switch_water_condition(nodes, frame_name, vol, links, label)
        # Switch water condition
        # frame = nodes.get(frame_name)
        # if not frame or frame.type != 'FRAME':
        #     print(f"Warning: frame '{frame_name}' not found or wrong type")
        #     continue

        # # Remove existing links
        # for inp in vol.inputs:
        #     for lnk in list(inp.links):
        #         links.remove(lnk)

        # vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
        # if len(vec_nodes) != 2:
        #     print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")
        #     continue

        # abs_node, scat_node = vec_nodes
        # try:
        #     links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
        #     links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])
        # except Exception as e:
        #     print(f"Failed to connect nodes for {frame_name}: {e}")
        #     continue

        # print(f"Switched water condition to {label}")


        z_offsets = func.choose_depth_type(water_type, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS)
        # Choose depth offset selection pool based on water type
        # if water_type == "Clear":
        #     z_offsets = CLEAR_Z_OFFSETS
        # else:
        #     z_offsets = MURKY_Z_OFFSETS


        # LOOP OVER Z OFFSETS
        for z in z_offsets:
            ocean_obj.location.z = z
            real_depth = func.blender_z_to_real_depth(z)

            print(f"Set Ocean Volume Z to: {real_depth} m depth")

            # -----------------------------
            # LOOP OVER RANDOM ARRANGEMENTS
            # -----------------------------
            for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
                
                func.rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX)
                # print(f"Random arrangement {arr_idx}")

                # # --- Initially disable all objects for render ---
                # for obj in all_objects:
                #     obj.hide_render = True

                # # --- randomly select objects ---
                # NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)  # 3-5 objects
                # selected_objects = random.sample(all_objects, NUM_OBJECTS)

                # # Randomize objects positions within foreground grid, keep original Z
                # for obj in selected_objects:
                #     obj.hide_render = False
                #     obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
                #     obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
                #     rot = random.uniform(0, 2*math.pi)
                #     obj.rotation_euler.z = rot
                

                if RENDER:
                    func.render_config(scene, temp_output, BASE_SAVE_PATH, cam_obj, frame_name, real_depth, arr_idx)

                    # # Render everything to the temp folder
                    # scene.render.filepath = temp_output + "/"
                    # bpy.ops.render.render(animation=True)

                    # # Move outputs to Camera/Water/Z/Arrangement folder
                    # cam_water_z_folder = os.path.join(
                    #     BASE_SAVE_PATH,
                    #     cam_obj.name,
                    #     frame_name,
                    #     f"Depth_{real_depth}m",
                    #     f"Arrangement_{arr_idx}"
                    # )
                    # os.makedirs(cam_water_z_folder, exist_ok=True)

                    # for item in os.listdir(temp_output):
                    #     src = os.path.join(temp_output, item)
                    #     dst = os.path.join(cam_water_z_folder, item)
                    #     if os.path.exists(dst):
                    #         if os.path.isdir(dst):
                    #             shutil.rmtree(dst)
                    #         else:
                    #             os.remove(dst)
                    #     shutil.move(src, dst)

                    # # Recreate temp folder for next render
                    # os.makedirs(temp_output, exist_ok=True)

                    # print(f"Saved outputs to: {cam_water_z_folder}")



print("\nDataset generation complete!")


























# # Generate dataset
# # See beginning of script for customisable features and render properties

# # ------ RUN INSTRUCTIONS ------
# # blender -b blender/underwater_scene.blend --python scripts/blender/generate_dataset.py


# # TO DO 
# # Make water lists one
# # Fix depth offset
# # Add in collision avoidance
# # Make subfunctions
# # Make two customisable sections 
# # Add in changing camera properties 
# # Size prediction at start 



# # Import libraries 
# import bpy
# import os
# import shutil
# import random
# import math

# # Import helper functions
# import helper_gen_dataset as h


# ## CUSTOMISE: RENDER PROPERTIES
# # Set render flag 
# RENDER = True

# # Define base export save path and temp output
# BASE_SAVE_PATH = "results/blender_output/"
# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# # Define the scene
# scene = bpy.context.scene

# # Define the number of frames to render per configuration 
# scene.frame_start = 1
# scene.frame_end = 1 # 30

# # Check the resolution 
# res_x = scene.render.resolution_x
# res_y = scene.render.resolution_y
# res_pct = scene.render.resolution_percentage

# # Compositor node tree
# tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")


# print("DATASET GENERATION FOR SIMULATED UNDERWATER SCENES\n")
# print("---RENDER PROPERTIES---")
# print(f"Number of frames per configuration: {scene.frame_end}")
# print(f"Renders will save into: {BASE_SAVE_PATH}")
# print(f"Render resolution: {res_x} x {res_y}")
# print(f"Resolution percentage: {res_pct}%")



# ## CUSTOMISE: DATASET FEATURES
# WATER_CONDITIONS = [
#     ("Jerlov",     "Jerlov I",   "Clear"),
#     ("Jerlov.001", "Jerlov IA",  "Clear"),
#     ("Jerlov.005", "Jerlov IB",  "Clear"),
#     ("Jerlov.004", "Jerlov II",  "Clear"),
#     ("Jerlov.003", "Jerlov IC",  "Clear"),   
#     ("Jerlov.002", "Jerlov III", "Murky"),
#     ("Jerlov.007", "Jerlov 5C",  "Murky"),
#     ("Jerlov.006", "Jerlov 3C",  "Murky"),
#     # ("Jerlov.008", "Jerlov 7C"),      # Too murky, can't see anything 
#     # ("Jerlov.009", "Jerlov 9C")
# ]

# # Define depths for Ocean Volume
# # Note: Offset of -25m in Blender = 0m depth e.g. -20m = 5m deep, -5m = 20m deep
# CLEAR_Z_OFFSETS = [-20, -5]
# MURKY_Z_OFFSETS = [-23]

# # Number of random arrangements environment configuration
# NUM_RANDOM_ARRANGEMENTS = 1 
# MIN_OBJECTS, MAX_OBJECTS = 3, 5

# # 3x3m grid bounds for Everyday Objects in foreground
# GRID_MIN = -1.5
# GRID_MAX = 1.5



# print("---DATASET FEATURES---")

# # Water conditions (human-readable only)
# print("Water conditions:")
# for _, label, _ in WATER_CONDITIONS:
#     print(f"  - {label}")

# # Depths (printed in real-world meters)
# print("Depths (real-world):")

# clear_depths = [h.blender_z_to_real_depth(z) for z in CLEAR_Z_OFFSETS]
# murky_depths = [h.blender_z_to_real_depth(z) for z in MURKY_Z_OFFSETS]

# print(f"  Clear water depths: {clear_depths} m")
# print(f"  Murky water depths: {murky_depths} m")

# # Object configuration
# print("Object placement:")
# print(f"  Objects per scene: {MIN_OBJECTS}–{MAX_OBJECTS}")
# print(f"  Random arrangements per configuration: {NUM_RANDOM_ARRANGEMENTS}")
# print(f"  Foreground grid: {GRID_MIN} m to {GRID_MAX} m (X/Y)")


# print("\nGenerating dataset!")
# print("With the current settings, this will take ~10 days, 2 hours to render")
# print("and use ~14.34 GB of storage.")
# print("Use Ctrl+C to cancel at any time.\n")





# # Confirmation prompt
# while True:
#     user_input = input("Proceed with dataset generation? (y/n): ").strip().lower()
#     if user_input in {"y", "yes"}:
#         print("Confirmed. Starting dataset generation\n")
#         print("Use Ctrl+C to cancel at anytime\n")
#         break
#     elif user_input in {"n", "no"}:
#         print("Dataset generation cancelled by user.")
#         raise SystemExit
#     else:
#         print("Please enter 'y' or 'n'.")





# # Get Ocean Volume and its volume coefficients for the water conditions
# MAT_NAME = "Ocean Volume"
# mat = bpy.data.materials.get(MAT_NAME)
# if not mat:
#     raise RuntimeError(f"Material '{MAT_NAME}' not found")

# nodes = mat.node_tree.nodes
# links = mat.node_tree.links
# vol = nodes.get("Volume Coefficients")
# if not vol:
#     raise RuntimeError("Volume Coefficients node not found")


# # Get collections
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




# # Extract all the everyday objects from their sub-collections
# all_objects = []
# for subcol in objects_collection.children:
#     all_objects.extend(subcol.objects)

# if len(all_objects) < MAX_OBJECTS:
#     raise RuntimeError("Not enough objects to sample from")




# # -----------------------------
# # MAIN LOOP: Cameras × Water × Z × Random Arrangement
# # -----------------------------
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"\n=== Camera: {cam_obj.name} ===")

#     for frame_name, label, water_type in WATER_CONDITIONS:
#         print(f"\n--- Water condition: {label} ({frame_name}) ---")

#         # Disable all lights first
#         for l in light_collection.objects:
#             l.hide_render = True

#         # Construct spotlight name
#         base_spot_name = cam_obj.name.replace("Camera", "Spot")
#         spotlight_name = f"{water_type} {base_spot_name}"
#         spotlight = light_collection.objects.get(spotlight_name)

#         # Enable correct spotlight
#         if spotlight:
#             spotlight.hide_render = False
#             print(f"Enabled light: {spotlight.name}")
#         else:
#             print(f"Warning: no matching {water_type} spotlight found for {cam_obj.name}")


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

#         # Choose depth offset selection pool based on water type
#         if water_type == "Clear":
#             z_offsets = CLEAR_Z_OFFSETS
#         else:
#             z_offsets = MURKY_Z_OFFSETS


#         # -----------------------------
#         # LOOP OVER Z OFFSETS
#         # -----------------------------
#         for z in z_offsets:
#             ocean_obj.location.z = z

#             real_depth = h.blender_z_to_real_depth(z)

#             # print(
#             #     f"Set Ocean Volume Z (Blender): {z} m | "
#             #     f"Real depth: {real_depth} m"
#             # )

#             print(f"Set Ocean Volume Z to: {real_depth} m depth")

#             # -----------------------------
#             # LOOP OVER RANDOM ARRANGEMENTS
#             # -----------------------------
#             for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
#                 print(f"Random arrangement {arr_idx}")

#                 # --- Initially disable all objects for render ---
#                 for obj in all_objects:
#                     obj.hide_render = True

#                 # --- randomly select objects ---
#                 NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)  # 3-5 objects
#                 selected_objects = random.sample(all_objects, NUM_OBJECTS)

#                 # Randomize objects positions within foreground grid, keep original Z
#                 for obj in selected_objects:
#                     obj.hide_render = False
#                     obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
#                     obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
#                     rot = random.uniform(0, 2*math.pi)
#                     obj.rotation_euler.z = rot
                

#                 if RENDER:
#                     # Render everything to the temp folder
#                     scene.render.filepath = temp_output + "/"
#                     bpy.ops.render.render(animation=True)

#                     # Move outputs to Camera/Water/Z/Arrangement folder
#                     cam_water_z_folder = os.path.join(
#                         BASE_SAVE_PATH,
#                         cam_obj.name,
#                         frame_name,
#                         f"Depth_{real_depth}m",
#                         f"Arrangement_{arr_idx}"
#                     )
#                     os.makedirs(cam_water_z_folder, exist_ok=True)

#                     for item in os.listdir(temp_output):
#                         src = os.path.join(temp_output, item)
#                         dst = os.path.join(cam_water_z_folder, item)
#                         if os.path.exists(dst):
#                             if os.path.isdir(dst):
#                                 shutil.rmtree(dst)
#                             else:
#                                 os.remove(dst)
#                         shutil.move(src, dst)

#                     # Recreate temp folder for next render
#                     os.makedirs(temp_output, exist_ok=True)

#                     print(f"Saved outputs to: {cam_water_z_folder}")



# print("\nAll camera x water x Z x random arrangement renders complete.")


















# # Generate dataset
# # See beginning of script for customisable features and render properties

# # ------ RUN INSTRUCTIONS ------
# # blender -b blender/underwater_scene.blend --python scripts/blender/generate_dataset.py


# # TO DO 
# # Make water lists one
# # Fix depth offset
# # Add in collision avoidance
# # Make subfunctions
# # Make two customisable sections 
# # Add in changing camera properties 
# # Size prediction at start 



# # Import libraries 
# import bpy
# import os
# import shutil
# import random
# import math

# ## CUSTOMISE: RENDER PROPERTIES
# RENDER = True

# # Define base export save path
# BASE_SAVE_PATH = "results/blender_output/"



# ## CUSTOMISE: DATASET FEATURES


# WATER_CONDITIONS = [
#     ("Jerlov",     "Jerlov I"),
#     ("Jerlov.001", "Jerlov IA"),
#     ("Jerlov.005", "Jerlov IB"),        # Clearest ones ^ 
#     ("Jerlov.004", "Jerlov II"),
#     ("Jerlov.003", "Jerlov IC"),        # Slightly murky but still clear. Use Clear camera spotlight ^ 
#     ("Jerlov.002", "Jerlov III"),       # Use Murky camera spotlight for this and below 
#     ("Jerlov.007", "Jerlov 5C"),
#     ("Jerlov.006", "Jerlov 3C")
#     # ("Jerlov.008", "Jerlov 7C"),      # Too murky, can't see anything 
#     # ("Jerlov.009", "Jerlov 9C")
# ]

# # COMBINE WITH WATER CONDITIONS SO ONE LIST 
# # Define water clarity type for the lights 
# # True = clear, False = murky
# CLEAR_WATER_FRAMES = ["Jerlov", "Jerlov.001", "Jerlov.005", "Jerlov.004", "Jerlov.003"]
# MURKY_WATER_FRAMES = ["Jerlov.002", "Jerlov.007", "Jerlov.006"]

# # Z offsets for Ocean Volume
# # Z_OFFSETS = [-20, -10, -5]
# # CHANGE TO OFFSET WITH 25 automatically 
# CLEAR_Z_OFFSETS = [-20, -10, -5]
# MURKY_Z_OFFSETS = [-23, -22]

# # MURKY_Z_OFFSETS = [-22, -21]


# # Number of random arrangements per camera × water × Z
# NUM_RANDOM_ARRANGEMENTS = 1 # 3
# MIN_OBJECTS, MAX_OBJECTS = 3, 5

# # 3x3 grid bounds for Everyday Objects in foreground
# GRID_MIN = -1.5
# GRID_MAX = 1.5

# # Get Ocean Volume and its volume coefficients for the water conditions
# MAT_NAME = "Ocean Volume"
# mat = bpy.data.materials.get(MAT_NAME)
# if not mat:
#     raise RuntimeError(f"Material '{MAT_NAME}' not found")

# nodes = mat.node_tree.nodes
# links = mat.node_tree.links
# vol = nodes.get("Volume Coefficients")
# if not vol:
#     raise RuntimeError("Volume Coefficients node not found")


# # Define the scene
# scene = bpy.context.scene

# # Get collections
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


# # Extract all the everyday objects from their sub-collections
# all_objects = []
# for subcol in objects_collection.children:
#     all_objects.extend(subcol.objects)

# if len(all_objects) < MAX_OBJECTS:
#     raise RuntimeError("Not enough objects to sample from")


# # Check resolution 
# res_x = scene.render.resolution_x
# res_y = scene.render.resolution_y
# res_pct = scene.render.resolution_percentage

# print(f"Render resolution: {res_x} x {res_y}")
# print(f"Resolution percentage: {res_pct}%")

# # -----------------------------
# # TEMP OUTPUT
# # -----------------------------
# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# scene.frame_start = 1
# scene.frame_end = 1

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

#     for frame_name, label in WATER_CONDITIONS:
#         print(f"\n--- Water condition: {label} ({frame_name}) ---")


#         ## SELECT CAMERA SPOTLIGHT IF CLEAR OR MURKY 
#         # Determine water clarity
#         if frame_name in CLEAR_WATER_FRAMES:
#             water_type = "Clear"
#         else:
#             water_type = "Murky"

#         # Disable all lights first
#         for l in light_collection.objects:
#             l.hide_render = True

#         # Construct spotlight name
#         base_spot_name = cam_obj.name.replace("Camera", "Spot")
#         spotlight_name = f"{water_type} {base_spot_name}"
#         spotlight = light_collection.objects.get(spotlight_name)

#         # Enable correct spotlight
#         if spotlight:
#             spotlight.hide_render = False
#             print(f"Enabled light: {spotlight.name}")
#         else:
#             print(f"Warning: no matching {water_type} spotlight found for {cam_obj.name}")


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

#         # Choose depth offset selection pool based on water type
#         if water_type == "Clear":
#             z_offsets = CLEAR_Z_OFFSETS
#         else:
#             z_offsets = MURKY_Z_OFFSETS


#         # -----------------------------
#         # LOOP OVER Z OFFSETS
#         # -----------------------------
#         for z in z_offsets:
#             ocean_obj.location.z = z
#             print(f"Set Ocean Volume Z to: {z} m")

#             # -----------------------------
#             # LOOP OVER RANDOM ARRANGEMENTS
#             # -----------------------------
#             for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
#                 print(f"Random arrangement {arr_idx}")

#                 # --- Initially disable all objects for render ---
#                 for obj in all_objects:
#                     obj.hide_render = True

#                 # --- randomly select objects ---
#                 NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)  # 3-5 objects
#                 selected_objects = random.sample(all_objects, NUM_OBJECTS)

#                 # Randomize objects positions within foreground grid, keep original Z
#                 for obj in selected_objects:
#                     obj.hide_render = False
#                     obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
#                     obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
#                     rot = random.uniform(0, 2*math.pi)
#                     obj.rotation_euler.z = rot
                

#                 if RENDER:
#                     # Render everything to the temp folder
#                     scene.render.filepath = temp_output + "/"
#                     bpy.ops.render.render(animation=True)

#                     # Move outputs to Camera/Water/Z/Arrangement folder
#                     cam_water_z_folder = os.path.join(
#                         BASE_SAVE_PATH,
#                         cam_obj.name,
#                         frame_name,
#                         f"Z_{z}m",
#                         f"Arrangement_{arr_idx}"
#                     )
#                     os.makedirs(cam_water_z_folder, exist_ok=True)

#                     for item in os.listdir(temp_output):
#                         src = os.path.join(temp_output, item)
#                         dst = os.path.join(cam_water_z_folder, item)
#                         if os.path.exists(dst):
#                             if os.path.isdir(dst):
#                                 shutil.rmtree(dst)
#                             else:
#                                 os.remove(dst)
#                         shutil.move(src, dst)

#                     # Recreate temp folder for next render
#                     os.makedirs(temp_output, exist_ok=True)

#                     print(f"Saved outputs to: {cam_water_z_folder}")



# print("\nAll camera x water x Z x random arrangement renders complete.")










