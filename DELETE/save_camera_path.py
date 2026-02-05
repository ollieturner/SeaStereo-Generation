

# UNTESTED 
# Inspired by https://blender.stackexchange.com/questions/58916/script-for-save-camera-position-to-file

# not sure why desgraph? 
# And frames?

import bpy
import os

print("Exporting camera trajectory...")

scene = bpy.context.scene
camera = bpy.context.active_object  # make sure camera is selected

if camera.type != 'CAMERA':
    raise RuntimeError("Active object is not a camera")

depsgraph = bpy.context.evaluated_depsgraph_get()

# Save next to the .blend file
blend_dir = bpy.path.abspath("//")
output_path = os.path.join(blend_dir, "camera_trajectory.csv")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("frame, x, y, z, rx, ry, rz\n")

    for frame in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(frame)

        cam_eval = camera.evaluated_get(depsgraph)
        mw = cam_eval.matrix_world

        loc = mw.to_translation()
        rot = mw.to_euler('XYZ')

        f.write(
            f"{frame}, "
            f"{loc.x:.6f}, {loc.y:.6f}, {loc.z:.6f}, "
            f"{rot.x:.6f}, {rot.y:.6f}, {rot.z:.6f}\n"
        )

print("Camera trajectory saved to:", output_path)
