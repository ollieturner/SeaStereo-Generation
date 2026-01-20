# NOT PRIORITY 

# Run with (from anywhere):
# blender -b /home/otur3695/Documents/Blender/mug_underwater_scene.blend   --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/change_water.py


# Naming convention: (done manually in blender)
# Name - Label
# Jerlov.002 - Jerlov III 
# Jerlov.004 - Jerlov II
# Jerlov - Jerlov I
# Jerlov.003 - Jerlov IC
# Jerlov.005 - Jerlov IB
# Jerlov.001 - Jerlov IA
# Jerlov.009 - Jerlov 9C
# Jerlov.008 - Jerlov 7C
# Jerlov.007 - Jerlov 5C
# Jerlov.006 - Jerlov 3C



# Iterate through each water condition (later: and render for each)
# But for now don't render, but just print out the current connections --> UNTESTED RENDERING but saving ok 
import bpy
import os

# -----------------------------
# CONFIG
# -----------------------------
MAT_NAME = "Ocean Volume"
BASE_SAVE_PATH = "/home/otur3695/Documents/Blender/results_7_1/test_water.blend"

# List of water conditions (Jerlov frames) in desired order
WATER_CONDITIONS = [
    ("Jerlov.002", "Jerlov III"),
    ("Jerlov.004", "Jerlov II"),
    ("Jerlov",     "Jerlov I"),
    ("Jerlov.003", "Jerlov IC"),
    ("Jerlov.005", "Jerlov IB"),
    ("Jerlov.001", "Jerlov IA"),
    ("Jerlov.009", "Jerlov 9C"),
    ("Jerlov.008", "Jerlov 7C"),
    ("Jerlov.007", "Jerlov 5C"),
    ("Jerlov.006", "Jerlov 3C")
]

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
# LOOP THROUGH WATER CONDITIONS
# -----------------------------
for frame_name, label in WATER_CONDITIONS:
    print(f"\n=== Switching to water condition: {label} ({frame_name}) ===")

    frame = nodes.get(frame_name)
    if not frame or frame.type != 'FRAME':
        print(f"Warning: frame '{frame_name}' not found or wrong type")
        continue

    # Remove existing links to Volume Coefficients
    for inp in vol.inputs:
        for l in list(inp.links):
            links.remove(l)

    # Get child Vector Math nodes (absorption + scattering)
    vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
    if len(vec_nodes) != 2:
        print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")
        continue

    # Deterministic order - Absorption, then Scatter
    abs_node = vec_nodes[0]
    scat_node = vec_nodes[1]

    # Connect them to Volume Coefficients
    try:
        links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])  # absorption
        links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])  # scattering
    except Exception as e:
        print(f"Failed to connect nodes for {frame_name}: {e}")
        continue

    # Print current connections
    print(f"Switched water condition to {label}")
    print("Absorption from:", abs_node.name)
    print("Scattering from:", scat_node.name)

    # Save a separate .blend for this condition
    save_path = BASE_SAVE_PATH.replace(".blend", f"_{frame_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=save_path)
    print(f"Saved Blender file to: {save_path}")

    # -----------------------------
    # OPTIONAL: Render animation
    # -----------------------------
    # Uncomment the following lines when you want to render:
    #
    # cam = scene.camera  # keep current active camera
    # cam_output_folder = save_path.replace(".blend", "")  # folder per water condition
    # os.makedirs(cam_output_folder, exist_ok=True)
    # scene.render.filepath = os.path.join(cam_output_folder, "")
    # bpy.ops.render.render(animation=True)
    # print(f"Rendered animation for {label} into {cam_output_folder}")

print("\nAll water conditions processed.")














# # Switch water condition from one to another, then save the file 
# import bpy

# MAT_NAME = "Ocean Volume"
# JERLOV_FRAME = "Jerlov.001"   # Jerlov.001 - Jerlov IA (target change)

# mat = bpy.data.materials.get(MAT_NAME)
# if not mat:
#     raise RuntimeError(f"Material '{MAT_NAME}' not found")

# nodes = mat.node_tree.nodes
# links = mat.node_tree.links

# vol = nodes.get("Volume Coefficients")
# if not vol:
#     raise RuntimeError("Volume Coefficients node not found")

# # Remove existing links to Volume Coefficients
# for inp in vol.inputs:
#     for l in list(inp.links):
#         links.remove(l)

# frame = nodes.get(JERLOV_FRAME)
# if not frame or frame.type != 'FRAME':
#     raise RuntimeError(f"Jerlov frame '{JERLOV_FRAME}' not found")

# # Get child Vector Math nodes in order
# vec_nodes = [
#     n for n in nodes
#     if n.parent == frame and n.type == 'VECT_MATH'
# ]

# if len(vec_nodes) != 2:
#     raise RuntimeError(
#         f"Expected 2 Vector Math nodes in {JERLOV_FRAME}, got {len(vec_nodes)}"
#     )

# # Deterministic order
# vec_nodes.sort(key=lambda n: n.name)

# # Print out Volume Coefficient inputs
# # for i, inp in enumerate(vol.inputs):
# #     print(i, inp.name, inp.identifier)

# abs_node = vec_nodes[0]
# scat_node = vec_nodes[1]

# links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
# links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])

# print(f"Switched water condition to {JERLOV_FRAME}")

# print("Absorption from:", abs_node.name)
# print("Scattering from:", scat_node.name)

# bpy.ops.wm.save_mainfile()











# ## Print out Jerlov water nodes in parent/child structure to confirm relationships
# import bpy

# mat = bpy.data.materials["Ocean Volume"]
# nodes = mat.node_tree.nodes

# for n in nodes:
#     if n.type == 'FRAME':
#         print(n.name)
#         for child in nodes:
#             if child.parent == n:
#                 print("  ", child.name)

# Output: 
# Jerlov
#    Vector Math
#    Vector Math.001
# Jerlov.001
#    Vector Math.002
#    Vector Math.003
# Jerlov.002
#    Vector Math.004
#    Vector Math.005
# Jerlov.003
#    Vector Math.006
#    Vector Math.007
# Jerlov.004
#    Vector Math.009
#    Vector Math.010
# Jerlov.005
#    Vector Math.011
#    Vector Math.012
# Jerlov.006
#    Vector Math.013
#    Vector Math.014
# Jerlov.007
#    Vector Math.015
#    Vector Math.016
# Jerlov.008
#    Vector Math.017
#    Vector Math.018
# Jerlov.009
#    Vector Math.019
#    Vector Math.020



## Print out all the nodes in Ocean Volume 
# import bpy

# mat = bpy.data.materials["Ocean Volume"]  
# tree = mat.node_tree

# print("Nodes in material:")
# for n in tree.nodes:
#     print(f"- {n.name}  [{n.type}]")
