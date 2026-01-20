# TO VERIFY 


# Make it just do one frame each 

# WRITE PLAN FIRST

# Make option at start to select all the options 
# Check against current render animation 




# # --- SELECTING AND RENDERING MULTIPLE CAMERAS ---

# NEW VERSION TO TEST:
# import bpy
# import os

# scene = bpy.context.scene

# camera_collection_name = "Cameras"
# camera_collection = bpy.data.collections.get(camera_collection_name)
# if not camera_collection:
#     raise RuntimeError(f"Collection '{camera_collection_name}' not found")

# output_base = "/home/otur3695/Documents/Blender/results/blender_output/"

# scene.frame_start = 1
# scene.frame_end = 1

# scene.use_nodes = True
# tree = scene.node_tree

# for cam_obj in camera_collection.objects:
#     if cam_obj.type != 'CAMERA':
#         continue

#     print(f"Rendering animation from camera: {cam_obj.name}")

#     scene.camera = cam_obj

#     cam_output_path = os.path.join(output_base, cam_obj.name)
#     os.makedirs(cam_output_path, exist_ok=True)

#     # Render Result output
#     scene.render.filepath = cam_output_path + "/"

#     # 🔑 Compositor File Output nodes
#     for node in tree.nodes:
#         if node.type == 'OUTPUT_FILE':
#             node.base_path = cam_output_path

#     bpy.ops.render.render(animation=True)

# print("All camera animations complete")


