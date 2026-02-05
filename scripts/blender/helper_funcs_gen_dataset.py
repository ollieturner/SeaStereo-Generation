import bpy
import os
import random
import math
import shutil
import mathutils  



def apply_render_props(BASE_SAVE_PATH, frame_start, frame_end, res_x, res_y, res_pct, tree_name):
    # Define base export save path and temp output
    temp_output = os.path.join(BASE_SAVE_PATH, "temp")
    os.makedirs(temp_output, exist_ok=True)

    # Define the scene
    scene = bpy.context.scene

    # Define the number of frames to render per configuration 
    scene.frame_start = frame_start # 1
    scene.frame_end = frame_end # 1 # 30

    # Define the resolution
    scene.render.resolution_x = res_x 
    scene.render.resolution_y = res_y 
    scene.render.resolution_percentage = res_pct

    # Set the compositor node tree
    tree = bpy.data.node_groups.get(tree_name)
    if not tree or tree.bl_idname != "CompositorNodeTree":
        raise RuntimeError(f"Compositor node tree '{tree_name}' not found or is not a compositor")

    return scene, temp_output



def get_collections():
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

    return camera_collection, light_collection, ocean_collection, objects_collection



def print_render_msg(RENDER, frame_end, BASE_SAVE_PATH, res_x, res_y, res_pct):
    print("DATASET GENERATION FOR SIMULATED UNDERWATER SCENES\n")
    print("---RENDER PROPERTIES---")
    print(f"Rendering enabled: {RENDER}")
    print(f"Number of frames per configuration: {frame_end}")
    print(f"Renders will save into: {BASE_SAVE_PATH}")
    print(f"Render resolution: {res_x} x {res_y}")
    print(f"Resolution percentage: {res_pct}%\n")


def blender_z_to_real_depth(z_blender):
    return z_blender + 25


def print_dataset_msg(camera_collection, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX):
    print("---DATASET FEATURES---")

    # List available cameras
    print("Available cameras:")
    if len(camera_collection.objects) == 0:
        print("  (No cameras found in 'Cameras' collection)")
    else:
        for obj in camera_collection.objects:
            if obj.type == 'CAMERA':
                print(f"  - {obj.name}")


    print("Camera types: ")
    print(f"  Focal lengths: {FOCAL_LENGTHS[0]}mm, {FOCAL_LENGTHS[1]}mm")
    print(f"  Interocular distances: {INTEROCULAR_DIST[0]}mm, {INTEROCULAR_DIST[1]}mm")

    # Water conditions (human-readable only)
    print("Water conditions:")
    for _, label, _ in WATER_CONDITIONS:
        print(f"  - {label}")

    # Depths (printed in real-world metres)
    print("Depths (real-world):")

    clear_depths = [blender_z_to_real_depth(z) for z in CLEAR_Z_OFFSETS]
    murky_depths = [blender_z_to_real_depth(z) for z in MURKY_Z_OFFSETS]

    print(f"  Clear water depths: {clear_depths} m")
    print(f"  Murky water depths: {murky_depths} m")

    # Object configuration
    print("Object placement:")
    print(f"  Objects per scene: {MIN_OBJECTS}–{MAX_OBJECTS}")
    print(f"  Random arrangements per configuration: {NUM_RANDOM_ARRANGEMENTS}")
    print(f"  Foreground grid: {GRID_MIN} m to {GRID_MAX} m (X/Y)")


def get_confirmation():
    print("\nWith the current settings, this will take ~10 days, 2 hours to render")
    print("and use ~14.34 GB of storage.")
    print("Use Ctrl+C to cancel at any time.\n")


    # Confirmation prompt
    while True:
        user_input = input("Proceed with dataset generation? (y/n): ").strip().lower()
        if user_input in {"y", "yes"}:
            print("Confirmed. Starting dataset generation\n")
            print("Use Ctrl+C to cancel at anytime\n")
            break
        elif user_input in {"n", "no"}:
            print("Dataset generation cancelled by user.")
            raise SystemExit
        else:
            print("Please enter 'y' or 'n'.")


def get_ocean_obj(ocean_collection):
    ocean_obj = ocean_collection.objects.get("Ocean Volume")
    if not ocean_obj:
        raise RuntimeError("Ocean Volume object not found in 'Ocean' collection")


    MAT_NAME = "Ocean Volume"
    mat = bpy.data.materials.get(MAT_NAME)
    if not mat:
        raise RuntimeError(f"Material '{MAT_NAME}' not found")

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    vol = nodes.get("Volume Coefficients")
    if not vol:
        raise RuntimeError("Volume Coefficients node not found")

    return ocean_obj, nodes, links, vol



def get_everyday_obj(objects_collection, MAX_OBJECTS):
    all_objects = []
    for subcol in objects_collection.children:
        all_objects.extend(subcol.objects)

    if len(all_objects) < MAX_OBJECTS:
        raise RuntimeError("Not enough objects to sample from")

    return all_objects


def get_camera(cam_obj, scene):
    if cam_obj.type != 'CAMERA':
        return False

    scene.camera = cam_obj
    return True



def set_camera_params(cam_obj, focal, interoc):
    # Set camera parameters
    cam_obj.data.lens = focal
    cam_obj.data.stereo.interocular_distance = interoc


def enable_spotlight(light_collection, cam_obj, water_type):
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
    else:
        print(f"Warning: no matching {water_type} spotlight found for {cam_obj.name}")

    return spotlight


def switch_water_condition(nodes, frame_name, vol, links, label):
    frame = nodes.get(frame_name)
    if not frame or frame.type != 'FRAME':
        print(f"Warning: frame '{frame_name}' not found or wrong type")

    # Remove existing links
    for inp in vol.inputs:
        for lnk in list(inp.links):
            links.remove(lnk)

    vec_nodes = [n for n in nodes if n.parent == frame and n.type == 'VECT_MATH']
    if len(vec_nodes) != 2:
        print(f"Warning: expected 2 Vector Math nodes in {frame_name}, got {len(vec_nodes)}")

    abs_node, scat_node = vec_nodes
    try:
        links.new(abs_node.outputs[0], vol.inputs["Absorption Coefficients"])
        links.new(scat_node.outputs[0], vol.inputs["Scatter Coefficients"])
    except Exception as e:
        print(f"Failed to connect nodes for {frame_name}: {e}")


def choose_depth_type(water_type, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS):
    if water_type == "Clear":
        z_offsets = CLEAR_Z_OFFSETS
    else:
        z_offsets = MURKY_Z_OFFSETS

    return z_offsets


# Randomly arrange objects and use AABB collision avoidance to prevent overlap - inspired by 
def rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX, MAX_TRIES=100):

    # Hide all objects initially
    for obj in all_objects:
        obj.hide_render = True
        # obj.hide_viewport = True  # Uncomment for Blender viewport

    NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)
    placed_objects = []  # track placed object AABBs
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    available_objects = all_objects.copy()
    random.shuffle(available_objects)
    
    objects_placed_count = 0

    # Loop until NUM_OBJECTS placed or all objects have been tried
    while available_objects and objects_placed_count < NUM_OBJECTS:
        obj = available_objects.pop(0)

        for _ in range(MAX_TRIES):
            # Random rotation
            obj.rotation_euler.z = random.uniform(0, 2 * math.pi)

            # Evaluate object with new rotation/scale
            eval_obj = obj.evaluated_get(depsgraph)

            # World-space bbox
            bbox = [eval_obj.matrix_world @ mathutils.Vector(corner)
                    for corner in eval_obj.bound_box]
            x_coords = [v.x for v in bbox]
            y_coords = [v.y for v in bbox]
            width = max(x_coords) - min(x_coords)
            depth = max(y_coords) - min(y_coords)

            # Random position within grid
            x = random.uniform(GRID_MIN + width / 2, GRID_MAX - width / 2)
            y = random.uniform(GRID_MIN + depth / 2, GRID_MAX - depth / 2)

            # Check overlap
            overlap = False
            for px, py, pw, pd in placed_objects:
                if abs(x - px) * 2 < (width + pw) and abs(y - py) * 2 < (depth + pd):
                    overlap = True
                    break

            # Place object if there's no overlap, otherwise try next one
            if not overlap:
                # Place object
                obj.location.x = x
                obj.location.y = y
                obj.hide_render = False
                # obj.hide_viewport = False  # Uncomment for Blender viewport

                placed_objects.append((x, y, width, depth))
                objects_placed_count += 1
                break

def print_render_config(cam_obj, focal, interoc, spotlight, label, frame_name, real_depth, arr_idx):
    print("\nRender with: ")
    print(f" {cam_obj.name}")
    print(f" Focal length: {focal}mm")
    print(f" Interocular distance: {interoc}mm")
    print(f" Enabled light: {spotlight.name}")
    print(f" Water condition: {label} ({frame_name})")
    print(f" Ocean volume depth: {real_depth} m")
    print(f" Random arrangement: {arr_idx}")

def render_config(scene, temp_output, BASE_SAVE_PATH, cam_obj, frame_name, real_depth, arr_idx, focal=None, interoc=None):
    scene.render.filepath = temp_output + "/"
    bpy.ops.render.render(animation=True)

    # Folder structure: Camera / Focal / Interocular / Water / Depth / Arrangement
    cam_water_z_folder = os.path.join(
        BASE_SAVE_PATH,
        cam_obj.name,
        f"Focal_{focal}mm",
        f"Interoc_{interoc}m",
        frame_name,
        f"Depth_{real_depth}m",
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

    os.makedirs(temp_output, exist_ok=True)
    print(f"Saved outputs to: {cam_water_z_folder}")

