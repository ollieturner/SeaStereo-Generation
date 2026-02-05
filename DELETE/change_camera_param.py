# NOT PRIORITY 

# Iterate through different combinations of values for camera parameters 
# RENDERNG UNTESTED 
# ASK ABOUT BOUNDS 
# Also ask which is necessary and how many cos this is a lot 

# blender -b /home/otur3695/Documents/Blender/mug_underwater_scene.blend   --python /home/otur3695/Documents/VRI_Underwater_Grasping/blender/change_camera_param.py


# PARAMETERS:
# Focal length
# Shift x ?
# Shift y ?
# Sensor width 
# Convergence (stereoscopy) (angle/tilt for convergence point)
# Interocular (stereoscopy) (separation of cameras)

# Clip min/max distance?
# Depth of field? Not enabled already 

# Current settings: 
# Focal length - 1.84mm
# Shift x - -0.099
# Shift y - -0.005
# Sensor width - 6.7mm
# Convergence (stereoscopy) - 1.95m (angle/tilt for convergence point)
# Interocular (stereoscopy) - 0.0577m (separation of cameras)

# Clip min/max distance? - 0.1 to 25m
# Depth of field? Not enabled already 


import bpy
import itertools

# -----------------------------
# CONFIG
# -----------------------------
CAM_COLLECTION = "Cameras"

# ARBITRARY NUMBERS 
# Parameter ranges
FOCAL_RANGE = [1.8, 2.0, 2.2]              # mm
SHIFT_X_RANGE = [-0.1, 0.0, 0.1]           # normalized
SHIFT_Y_RANGE = [-0.01, 0.0, 0.01]         # normalized
SENSOR_WIDTH_RANGE = [6.7, 8.0]            # mm
CONVERGENCE_RANGE = [1.9, 2.0, 2.1]        # m
INTEROCULAR_RANGE = [0.057, 0.058, 0.059]  # m

# Clip distances
CLIP_START = 0.1
CLIP_END = 25.0

# -----------------------------
# GET CAMERAS
# -----------------------------
cam_collection = bpy.data.collections.get(CAM_COLLECTION)
if not cam_collection:
    raise RuntimeError(f"Collection '{CAM_COLLECTION}' not found")

cameras = [obj for obj in cam_collection.objects if obj.type == "CAMERA"]
if not cameras:
    raise RuntimeError(f"No cameras found in collection '{CAM_COLLECTION}'")

# -----------------------------
# ITERATE OVER CAMERAS AND PARAMETER COMBINATIONS
# -----------------------------
for cam_obj in cameras:
    cam = cam_obj.data  # camera data block
    print(f"\n=== Camera: {cam_obj.name} ===")

    # Iterate over all combinations of the ranges
    for focal, shift_x, shift_y, sensor_w, conv, interoc in itertools.product(
        FOCAL_RANGE,
        SHIFT_X_RANGE,
        SHIFT_Y_RANGE,
        SENSOR_WIDTH_RANGE,
        CONVERGENCE_RANGE,
        INTEROCULAR_RANGE
    ):
        # Set camera parameters
        cam.lens = focal
        cam.shift_x = shift_x
        cam.shift_y = shift_y
        cam.sensor_width = sensor_w
        cam.clip_start = CLIP_START
        cam.clip_end = CLIP_END

        # TODO: delete this if
        if hasattr(cam, "stereo"):  # only if stereo camera
            cam.stereo.convergence_distance = conv
            cam.stereo.interocular_distance = interoc

        # Optional: print out the current combination
        print(f"Focal: {focal}mm, ShiftX: {shift_x}, ShiftY: {shift_y}, "
              f"Sensor: {sensor_w}mm, Conv: {conv}m, Interocular: {interoc}m")

        # -----------------------------
        # OPTIONAL: set active camera and render
        # -----------------------------
        # bpy.context.scene.camera = cam_obj
        # output_folder = f"/path/to/output/{cam_obj.name}/f{focal}_sx{shift_x}_sy{shift_y}_sw{sensor_w}_c{conv}_i{interoc}/"
        # os.makedirs(output_folder, exist_ok=True)
        # bpy.context.scene.render.filepath = os.path.join(output_folder, "")
        # bpy.ops.render.render(animation=True)
