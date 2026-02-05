# Generate dataset
# See beginning of script for customisable features and render properties

# ------ RUN INSTRUCTIONS ------
# blender -b blender/underwater_scene.blend --python scripts/blender/generate_dataset.py


# TO DO 
# Add in collision avoidance
# Add in changing camera properties 


# Import libraries 
import os
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


# Get collections from Blender file
camera_collection, light_collection, ocean_collection, objects_collection = func.get_collections()

# Printing messages to terminal and asking for user confirmation
func.print_render_msg(RENDER, frame_end, BASE_SAVE_PATH, res_x, res_y, res_pct)
func.print_dataset_msg(camera_collection, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX)
func.get_confirmation()


# Get the ocean volume object and initial nodes, links for water conditions
ocean_obj, nodes, links, vol = func.get_ocean_obj(ocean_collection)

# Get the everyday objects into a list for randomisation later
all_objects = func.get_everyday_obj(objects_collection, MAX_OBJECTS)

## MAIN LOOP OVER CONFIGURATIONS
# Start with cameras 
for cam_obj in camera_collection.objects:
    # Select object and continue if camera
    if not func.get_camera(cam_obj, scene):
        continue

    # Iterate over water conditions
    for frame_name, label, water_type in WATER_CONDITIONS:
        print(f"\n--- Water condition: {label} ({frame_name}) ---")

        func.enable_spotlight(light_collection, cam_obj, water_type)

        func.switch_water_condition(nodes, frame_name, vol, links, label)
        
        # Select either CLEAR or MURKY depths
        z_offsets = func.choose_depth_type(water_type, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS)

        # Iterate over Z depths
        for z in z_offsets:
            ocean_obj.location.z = z
            real_depth = func.blender_z_to_real_depth(z)

            print(f"Set Ocean Volume Z to: {real_depth} m depth")

            # Iterate over number of random arrangements
            for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
                
                func.rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX)

                # Render the courrent configuration
                if RENDER:
                    func.render_config(scene, temp_output, BASE_SAVE_PATH, cam_obj, frame_name, real_depth, arr_idx)

# Finished
print("\nDataset generation complete!")

