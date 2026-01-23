# TO VERIFY 


# Make it just do one frame each 

# WRITE PLAN FIRST

# Make option at start to select all the options 
# Check against current render animation 


# blender -b /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender/underwater_scene.blend \
#         --python /home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/scripts/blender/generate_sample_dataset.py




# --- SELECTING AND RENDERING MULTIPLE CAMERAS ---

# Render into normal folder then move files 
# Had trouble trying to change where the compositing nodes saved


# Select cameras

# Select corresponding spot light in lights collection 

# Then add a layer to iterate over water conditions 

# Then add a layer to iterate over depths 





# CAMERAS + LIGHTS + DEPTH + WATER + ARRANGEMENTS

# CAMERA × WATER × Z × RANDOM ARRANGEMENTS + LIGHTS + OBJECTS
import bpy
import os
import shutil
import random

# -----------------------------
# CONFIG
# -----------------------------
MAT_NAME = "Ocean Volume"
BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results/blender_output/"

# Water conditions (name, label)
WATER_CONDITIONS = [
    ("Jerlov",     "Jerlov I"),     
    # ("Jerlov.004", "Jerlov II"),
    # ("Jerlov.002", "Jerlov III"),
    ("Jerlov.001", "Jerlov IA"),
    ("Jerlov.005", "Jerlov IB"),
]

# Z offsets for Ocean Volume
Z_OFFSETS = [-20, -10, -5]

# Number of random arrangements per camera × water × Z
NUM_RANDOM_ARRANGEMENTS = 3

# 2x2 grid bounds for objects
GRID_MIN = -1.0
GRID_MAX = 1.0

# -----------------------------
# GET MATERIAL (Ocean Volume)
# -----------------------------
mat = bpy.data.materials.get(MAT_NAME)
if not mat:
    raise RuntimeError(f"Material '{MAT_NAME}' not found")

nodes = mat.node_tree.nodes
links = mat.node_tree.links
vol = nodes.get("Volume Coefficients")
if not vol:
    raise RuntimeError("Volume Coefficients node not found")

# -----------------------------
# COLLECTIONS
# -----------------------------
scene = bpy.context.scene
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

# -----------------------------
# TEMP OUTPUT
# -----------------------------
temp_output = os.path.join(BASE_SAVE_PATH, "temp")
os.makedirs(temp_output, exist_ok=True)

scene.frame_start = 1
scene.frame_end = 1 # CHANGE TO 2030

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

    # Disable all camera lights first
    for l in light_collection.objects:
        l.hide_render = True

    # Enable matching spotlight
    spotlight_name = cam_obj.name.replace("Camera", "Spot")
    spotlight = light_collection.objects.get(spotlight_name)
    if spotlight:
        spotlight.hide_render = False
        print(f"Enabled light: {spotlight.name}")
    else:
        print(f"Warning: no matching spotlight found for {cam_obj.name}")

    for frame_name, label in WATER_CONDITIONS:
        print(f"\n--- Water condition: {label} ({frame_name}) ---")

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

                # Randomize objects positions within 2x2 grid, keep original Z
                for obj in objects_collection.objects:
                    obj.location.x = random.uniform(GRID_MIN, GRID_MAX)
                    obj.location.y = random.uniform(GRID_MIN, GRID_MAX)
                    # Z stays the same
                
                # TODO Make sure not clashing based on bounding box min/maxes

                # Render everything to the temp folder
                render_temp = os.path.join(temp_output, "delete_global")
                os.makedirs(render_temp, exist_ok=True)
                scene.render.filepath = render_temp + "/"
                bpy.ops.render.render(animation=True)

                # -----------------------------
                # DELETE ONLY delete_global FOLDER
                # -----------------------------
                if os.path.exists(render_temp):
                    shutil.rmtree(render_temp)
                    print(f"Deleted temporary global render folder: {render_temp}")

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

    # Disable spotlight after camera is done
    if spotlight:
        spotlight.hide_render = True

print("\nAll camera × water × Z × random arrangement renders complete.")










































# # CAMERA × WATER × Z + LIGHTS
# import bpy
# import os
# import shutil

# # -----------------------------
# # CONFIG
# # -----------------------------
# MAT_NAME = "Ocean Volume"
# BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results/blender_output/"

# # name - label
# WATER_CONDITIONS = [
#     ("Jerlov",     "Jerlov I"),  # DO THIS ONE   
#     # ("Jerlov.004", "Jerlov II"),
#     # ("Jerlov.002", "Jerlov III"),
#     ("Jerlov.001", "Jerlov IA"),
#     ("Jerlov.005", "Jerlov IB") # ,  # NORMAL ONE
#     # ("Jerlov.003", "Jerlov IC"),
#     # ("Jerlov.006", "Jerlov 3C"),
#     # ("Jerlov.007", "Jerlov 5C"),
#     # ("Jerlov.008", "Jerlov 7C"),
#     # ("Jerlov.009", "Jerlov 9C")      
# ]

# # Z offsets for Ocean Volume
# Z_OFFSETS = [-20, -10, -5]

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
# # CAMERA & LIGHT COLLECTIONS
# # -----------------------------
# scene = bpy.context.scene
# camera_collection = bpy.data.collections.get("Cameras")
# light_collection = bpy.data.collections.get("Camera Lights")
# ocean_collection = bpy.data.collections.get("Ocean")

# if not camera_collection:
#     raise RuntimeError("Camera collection not found")
# if not light_collection:
#     raise RuntimeError("Lights collection not found")
# if not ocean_collection:
#     raise RuntimeError("Ocean collection not found")

# ocean_obj = ocean_collection.objects.get("Ocean Volume")
# if not ocean_obj:
#     raise RuntimeError("Ocean Volume object not found in 'Ocean' collection")

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
# # MAIN LOOP: Cameras × Water × Z
# # -----------------------------
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"\n=== Camera: {cam_obj.name} ===")

#     # Disable all lights first
#     for l in light_collection.objects:
#         l.hide_render = True

#     # Try to find the matching spotlight
#     spotlight_name = cam_obj.name.replace("Camera", "Spot")  # mapping rule
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

#             # Render everything to the temp folder
#             render_temp = os.path.join(temp_output, "delete_global")
#             os.makedirs(render_temp, exist_ok=True)
#             scene.render.filepath = render_temp + "/"
#             bpy.ops.render.render(animation=True)

#             # Move outputs to camera/water/Z folder
#             cam_water_z_folder = os.path.join(BASE_SAVE_PATH, cam_obj.name, frame_name, f"Z_{z}m")
#             os.makedirs(cam_water_z_folder, exist_ok=True)

#             for item in os.listdir(temp_output):
#                 src = os.path.join(temp_output, item)
#                 dst = os.path.join(cam_water_z_folder, item)
#                 if os.path.exists(dst):
#                     if os.path.isdir(dst):
#                         shutil.rmtree(dst)
#                     else:
#                         os.remove(dst)
#                 shutil.move(src, dst)

#             # Recreate temp folder for next render
#             os.makedirs(temp_output, exist_ok=True)

#             print(f"Saved outputs to: {cam_water_z_folder}")

#     # Disable spotlight after camera is done
#     if spotlight:
#         spotlight.hide_render = True

# print("\nAll camera × water × Z renders complete.")
























# # CAMERA _ WATER + LIGHTS 
# import bpy
# import os
# import shutil

# # -----------------------------
# # CONFIG
# # -----------------------------
# MAT_NAME = "Ocean Volume"
# BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results/blender_output/"
# # name - label
# WATER_CONDITIONS = [
#     ("Jerlov",     "Jerlov I"),     
#     # ("Jerlov.004", "Jerlov II"),
#     # ("Jerlov.002", "Jerlov III"),
#     ("Jerlov.001", "Jerlov IA"),
#     ("Jerlov.005", "Jerlov IB"),
#     # ("Jerlov.003", "Jerlov IC"),
#     # ("Jerlov.006", "Jerlov 3C"),
#     # ("Jerlov.007", "Jerlov 5C"),
#     # ("Jerlov.008", "Jerlov 7C"),
#     # ("Jerlov.009", "Jerlov 9C")      
# ]

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
# # CAMERA & LIGHT COLLECTIONS
# # -----------------------------
# scene = bpy.context.scene
# camera_collection = bpy.data.collections.get("Cameras")
# light_collection = bpy.data.collections.get("Lights")

# if not camera_collection:
#     raise RuntimeError("Camera collection not found")
# if not light_collection:
#     raise RuntimeError("Lights collection not found")

# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# scene.frame_start = 1
# scene.frame_end = 1

# tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

# # -----------------------------
# # MAIN LOOP: Cameras × Water Conditions
# # -----------------------------
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"\n=== Camera: {cam_obj.name} ===")

#     # Disable all lights first
#     for l in light_collection.objects:
#         l.hide_render = True

#     # Try to find the matching spotlight
#     spotlight_name = cam_obj.name.replace("Camera", "Spot")  # simple mapping rule
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


#         # print(f"[DEBUG] Would render camera: {cam_obj.name}, water: {label}")

#         # -----------------------------
#         # RENDER
#         # -----------------------------
#         render_temp = os.path.join(temp_output, "delete_global")
#         os.makedirs(render_temp, exist_ok=True)
#         scene.render.filepath = render_temp + "/"
#         bpy.ops.render.render(animation=True)

#         # -----------------------------
#         # MOVE OUTPUTS TO CAMERA/WATER FOLDER
#         # -----------------------------
#         cam_water_folder = os.path.join(BASE_SAVE_PATH, cam_obj.name, frame_name)
#         os.makedirs(cam_water_folder, exist_ok=True)

#         for item in os.listdir(temp_output):
#             src = os.path.join(temp_output, item)
#             dst = os.path.join(cam_water_folder, item)
#             if os.path.exists(dst):
#                 if os.path.isdir(dst):
#                     shutil.rmtree(dst)
#                 else:
#                     os.remove(dst)
#             shutil.move(src, dst)

#         # Recreate temp folder for next water condition
#         os.makedirs(temp_output, exist_ok=True)

#         print(f"Saved outputs to: {cam_water_folder}")

#     # Disable the spotlight after this camera is done
#     if spotlight:
#         spotlight.hide_render = True

# print("\nAll camera × water condition renders complete.")











# CAMERA + WATER NO LIGHT
# import bpy
# import os
# import shutil

# # -----------------------------
# # CONFIG
# # -----------------------------

# MAT_NAME = "Ocean Volume"
# BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results/blender_output/"

# # name - label
# WATER_CONDITIONS = [
#     # ("Jerlov",     "Jerlov I"),     # clearest
#     # ("Jerlov.004", "Jerlov II"),
#     ("Jerlov.002", "Jerlov III"),
#     # ("Jerlov.001", "Jerlov IA"),
#     ("Jerlov.005", "Jerlov IB"),
#     # ("Jerlov.003", "Jerlov IC"),
#     # ("Jerlov.006", "Jerlov 3C"),
#     # ("Jerlov.007", "Jerlov 5C"),
#     # ("Jerlov.008", "Jerlov 7C"),
#     ("Jerlov.009", "Jerlov 9C")      # darkest
# ]

# # WATER_CONDITIONS = [
# #     ("Jerlov",     "Jerlov I"),     # clearest
# #     ("Jerlov.004", "Jerlov II"),
# #     ("Jerlov.002", "Jerlov III"),
# #     ("Jerlov.001", "Jerlov IA"),
# #     ("Jerlov.005", "Jerlov IB"),
# #     ("Jerlov.003", "Jerlov IC"),
# #     ("Jerlov.006", "Jerlov 3C"),
# #     ("Jerlov.007", "Jerlov 5C"),
# #     ("Jerlov.008", "Jerlov 7C"),
# #     ("Jerlov.009", "Jerlov 9C")      # darkest
# # ]



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
# # CAMERA COLLECTION
# # -----------------------------
# scene = bpy.context.scene
# camera_collection = bpy.data.collections.get("Cameras")
# if not camera_collection:
#     raise RuntimeError("Camera collection not found")

# temp_output = os.path.join(BASE_SAVE_PATH, "temp")
# os.makedirs(temp_output, exist_ok=True)

# scene.frame_start = 1
# scene.frame_end = 1

# tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

# # -----------------------------
# # MAIN LOOP: Cameras × Water Conditions
# # -----------------------------
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"\n=== Camera: {cam_obj.name} ===")

#     for frame_name, label in WATER_CONDITIONS:
#         print(f"\n--- Water condition: {label} ({frame_name}) ---")

#         # Switch water condition by reconnecting material nodes
#         frame = nodes.get(frame_name)
#         if not frame or frame.type != 'FRAME':
#             print(f"Warning: frame '{frame_name}' not found or wrong type")
#             continue

#         # Remove existing links to Volume Coefficients
#         for inp in vol.inputs:
#             for l in list(inp.links):
#                 links.remove(l)

#         # Get child Vector Math nodes (absorption + scattering)
#         vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
#         if len(vec_nodes) != 2:
#             print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")
#             continue

#         # Absorption, then Scatter
#         abs_node = vec_nodes[0]
#         scat_node = vec_nodes[1]

#         try:
#             links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
#             links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])
#         except Exception as e:
#             print(f"Failed to connect nodes for {frame_name}: {e}")
#             continue

#         print(f"Switched water condition to {label}")

#         # -----------------------------
#         # RENDER
#         # -----------------------------
#         # Render everything to the temp folder
#         render_temp = os.path.join(temp_output, "delete_global")
#         os.makedirs(render_temp, exist_ok=True)
#         scene.render.filepath = render_temp + "/"
#         bpy.ops.render.render(animation=True)

#         # -----------------------------
#         # MOVE OUTPUTS TO CAMERA/WATER FOLDER
#         # -----------------------------
#         cam_water_folder = os.path.join(BASE_SAVE_PATH, cam_obj.name, frame_name)
#         os.makedirs(cam_water_folder, exist_ok=True)

#         for item in os.listdir(temp_output):
#             src = os.path.join(temp_output, item)
#             dst = os.path.join(cam_water_folder, item)
#             if os.path.exists(dst):
#                 if os.path.isdir(dst):
#                     shutil.rmtree(dst)
#                 else:
#                     os.remove(dst)
#             shutil.move(src, dst)

#         # Recreate temp folder for next water condition
#         os.makedirs(temp_output, exist_ok=True)

#         print(f"Saved outputs to: {cam_water_folder}")

# print("\nAll camera, water condition renders complete.")




















# import bpy
# import os
# import shutil

# scene = bpy.context.scene
# camera_collection = bpy.data.collections.get("Cameras")
# if not camera_collection:
#     raise RuntimeError("Camera collection not found")

# output_base = "/home/otur3695/Documents/Blender/results/blender_output/"
# temp_output = os.path.join(output_base, "temp")
# os.makedirs(temp_output, exist_ok=True)

# scene.frame_start = 1
# scene.frame_end = 1

# # Select CompositingNodeTree group to do correct render 
# tree_name = "Render Output"
# tree = bpy.data.node_groups.get(tree_name)
# if not tree or tree.bl_idname != "CompositorNodeTree":
#     raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

# # Iterate over camera collection 
# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     scene.camera = cam_obj
#     print(f"Rendering camera: {cam_obj.name}")

#     # Render everything to the temp folder
#     scene.render.filepath = os.path.join(temp_output, "delete_global") + "/"
#     bpy.ops.render.render(animation=True)

#     # After render, move everything from temp folder into camera folder
#     cam_folder = os.path.join(output_base, cam_obj.name)
#     os.makedirs(cam_folder, exist_ok=True)

#     # Move all files and subfolders inside temp into camera folder
#     for item in os.listdir(temp_output):
#         src = os.path.join(temp_output, item)
#         dst = os.path.join(cam_folder, item)
#         if os.path.exists(dst):
#             # If destination exists, remove it first
#             if os.path.isdir(dst):
#                 shutil.rmtree(dst)
#             else:
#                 os.remove(dst)
#         shutil.move(src, dst)

#     print(f"Moved render outputs to: {cam_folder}")

#     # Recreate temp folder for next camera
#     os.makedirs(temp_output, exist_ok=True)

# print("All camera animations complete")

