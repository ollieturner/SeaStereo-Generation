# Generate dataset
# See beginning of script for customisable features and render properties

# ------ RUN INSTRUCTIONS ------
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/generate_dataset.py


# Import libraries 
import os
import sys
import itertools
import random

# Define the script directory to import helper functions 
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import helper_funcs_gen_dataset as func


##############################
# SAVE_SHAPENET_OBJS = False  # ONLY True once

SHAPENET_TXT = "shapenet_paths.txt"

# if SAVE_SHAPENET_OBJS:
#     func.precompute_shapenet_paths(
#         "blender_scene/everyday objects/ShapeNet_objects",
#         SHAPENET_TXT
#     )
#     print("Precompute complete. Set SAVE_SHAPENET_OBJS=False and rerun.")
#     sys.exit()

ALL_OBJ_PATHS = func.load_shapenet_paths(SHAPENET_TXT)
##############################





## CUSTOMISE: RENDER PROPERTIES
RENDER = True
BASE_SAVE_PATH = "results/blender_output/"
frame_start = 1
frame_end = 30
res_x = 640
res_y = 480
res_pct = 100
tree_name = "Render Output"

scene, temp_output = func.apply_render_props(BASE_SAVE_PATH, frame_start, frame_end, res_x, res_y, res_pct, tree_name)


## CUSTOMISE: DATASET FEATURES
FOCAL_LENGTHS = [1.5, 2.5]
INTEROCULAR_DIST = [0.04, 0.08]

WATER_CONDITIONS = [
    ("Jerlov",     "Jerlov I",   "Clear"),
    ("Jerlov.001", "Jerlov IA",  "Clear"),
    ("Jerlov.005", "Jerlov IB",  "Clear"),
    ("Jerlov.004", "Jerlov II",  "Clear"),
    ("Jerlov.003", "Jerlov IC",  "Clear"),   
    ("Jerlov.002", "Jerlov III", "Murky"),
    ("Jerlov.007", "Jerlov 5C",  "Murky"),
    ("Jerlov.006", "Jerlov 3C",  "Murky")
    # ("Jerlov.008", "Jerlov 7C"),      # Too murky, can't see anything 
    # ("Jerlov.009", "Jerlov 9C")
]

# Define depths for Ocean Volume
# Note: Offset of -25m in Blender = 0m depth e.g. -20m = 5m deep, -5m = 20m deep
# CLEAR_Z_OFFSETS = [-20, -5]
# MURKY_Z_OFFSETS = [-23]

# Murky water depth range
MURKY_DEPTH_RANGE = (-23, -21)  # deeper negative = deeper in Blender

# Shallow water: select one deep, one shallow
CLEAR_DEEP_RANGE = (-10, -5)   # “deep” shallow
CLEAR_SHALLOW_RANGE = (-20, -15)  # “shallow” shallow



# Number of random arrangements environment configuration
NUM_RANDOM_ARRANGEMENTS = 1 
MIN_OBJECTS, MAX_OBJECTS = 3, 5

# 3x3m grid bounds for Everyday Objects in foreground
GRID_MIN = -1.5
GRID_MAX = 1.5


# Get collections from Blender file
camera_collection, light_collection, ocean_collection, objects_collection = func.get_collections()

# Printing messages to terminal and asking for user confirmation
func.print_render_msg(RENDER, frame_end, BASE_SAVE_PATH, res_x, res_y, res_pct)
func.print_dataset_msg(camera_collection, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX)
func.get_confirmation()

# Get the ocean volume object and initial nodes, links for water conditions
ocean_obj, nodes, links, vol = func.get_ocean_obj(ocean_collection)

# # Get the everyday objects into a list for randomisation later
# all_objects = func.get_everyday_obj(objects_collection, MAX_OBJECTS)

def get_random_shapenet_paths(all_paths, MIN_OBJECTS, MAX_OBJECTS):
    num_objects = random.randint(MIN_OBJECTS, MAX_OBJECTS)
    return random.sample(all_paths, num_objects)

## MAIN LOOP OVER CONFIGURATIONS
# Start with cameras 
for cam_obj in camera_collection.objects:
    # Select object and continue if camera
    if not func.get_camera(cam_obj, scene):
        continue

    # Iterate over camera types
    for focal, interoc in itertools.product(FOCAL_LENGTHS, INTEROCULAR_DIST):
        # Set the camera parameters (focal length, interocular distance)
        func.set_camera_params(cam_obj, focal, interoc)

        # Iterate over water conditions
        for frame_name, label, water_type in WATER_CONDITIONS:
            # Choose the correct spotlight for the clear/murky water
            spotlight = func.enable_spotlight(light_collection, cam_obj, water_type)

            # Switch the water condition
            func.switch_water_condition(nodes, frame_name, vol, links, label)
            
            # # Select either CLEAR or MURKY depths
            # z_offsets = func.choose_depth_type(water_type, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS)

            # # Iterate over Z depths
            # for z in z_offsets:
            #     ocean_obj.location.z = z

            z_offsets = func.choose_depth_type_new(
                water_type,
                CLEAR_DEEP_RANGE,
                CLEAR_SHALLOW_RANGE,
                MURKY_DEPTH_RANGE
            )

            for z in z_offsets:
                ocean_obj.location.z = z

                real_depth = func.blender_z_to_real_depth(z)

                # Iterate over number of random arrangements
                for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
                    
                    # # Randomly arrange the object with AABB collision avoidance
                    # func.rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX)

                    # Choose a random number of objects to arrange
                    NUM_OBJECTS = random.randint(MIN_OBJECTS, MAX_OBJECTS)

                    func.import_and_try_place(
                        ALL_OBJ_PATHS,
                        NUM_OBJECTS,
                        GRID_MIN,
                        GRID_MAX,
                        MAX_TRIES=100,
                        scale_factor=1.5,
                        z_height=-1
                    )


                    # Print out the current configuration settings to terminal
                    func.print_render_config(cam_obj, focal, interoc, spotlight, label, frame_name, real_depth, arr_idx)

                    # Render the courrent configuration
                    if RENDER:
                        func.render_config(scene, temp_output, BASE_SAVE_PATH, cam_obj, frame_name, real_depth, arr_idx, focal=focal, interoc=interoc)

                    func.delete_all_imported_objects()

# Finished
print("\nDataset generation complete!")

