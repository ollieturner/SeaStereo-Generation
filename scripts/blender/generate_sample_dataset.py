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




import bpy
import os
import shutil

scene = bpy.context.scene
camera_collection = bpy.data.collections.get("Cameras")
if not camera_collection:
    raise RuntimeError("Camera collection not found")

output_base = "/home/otur3695/Documents/Blender/results/blender_output/"
temp_output = os.path.join(output_base, "temp")
os.makedirs(temp_output, exist_ok=True)

scene.frame_start = 1
scene.frame_end = 1

tree_name = "Render Output"
tree = bpy.data.node_groups.get(tree_name)
if not tree or tree.bl_idname != "CompositorNodeTree":
    raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

for cam_obj in camera_collection.objects:
    if cam_obj.type != 'CAMERA':
        continue

    scene.camera = cam_obj
    print(f"Rendering camera: {cam_obj.name}")

    # Render everything to the temp folder
    scene.render.filepath = os.path.join(temp_output, "delete_global") + "/"
    bpy.ops.render.render(animation=True)

    # After render, move everything from temp folder into camera folder
    cam_folder = os.path.join(output_base, cam_obj.name)
    os.makedirs(cam_folder, exist_ok=True)

    # Move all files and subfolders inside temp into camera folder
    for item in os.listdir(temp_output):
        src = os.path.join(temp_output, item)
        dst = os.path.join(cam_folder, item)
        if os.path.exists(dst):
            # If destination exists, remove it first
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        shutil.move(src, dst)

    print(f"Moved render outputs to: {cam_folder}")

    # Recreate temp folder for next camera
    os.makedirs(temp_output, exist_ok=True)

print("All camera animations complete")

