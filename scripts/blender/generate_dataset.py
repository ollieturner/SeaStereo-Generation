# Generate dataset
# See beginning of script for customisable features and render properties

# Currently running without confirmation to allow running in background from SSH 

# ------ RUN INSTRUCTIONS ------
# Run generate dataset script with blender in background
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/generate_dataset.py
# Run above but with terminal output saved to file:
# blender -b blender_scene/underwater_scene.blend --python scripts/blender/generate_dataset.py > output.log 2>&1

# Import libraries 
import os
import sys
import itertools

# Define the script directory to import helper functions 
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import helper_funcs_gen_dataset as func


## CUSTOMISE: RENDER PROPERTIES
RENDER = True
BASE_SAVE_PATH = "results/blender_output/"
frame_start = 1
frame_end = 40
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
    ("Jerlov.003", "Jerlov IC",  "Clearish"),  
    ("Jerlov.004", "Jerlov II",  "Clearish"),
    ("Jerlov.002", "Jerlov III", "Murky"),
    ("Jerlov.006", "Jerlov 3C",  "Murky")
    # ("Jerlov.007", "Jerlov 5C",  "Murky"), # Too murky, can't see anything 
    # ("Jerlov.008", "Jerlov 7C", "Murky"),      
    # ("Jerlov.009", "Jerlov 9C", "Murky")
]

# Define depths for Ocean Volume
# Note: Offset of -25m in Blender = 0m depth e.g. -20m = 5m deep, -5m = 20m deep
MURKY_SHALLOW_RANGE = (-23.3, -22.7)  
CLEAR_DEEP_RANGE = (-10, -5)   
CLEAR_SHALLOW_RANGE = (-20, -15)  

# Number of random arrangements environment configuration
NUM_RANDOM_ARRANGEMENTS = 3 
MIN_OBJECTS, MAX_OBJECTS = 3, 5

# 3x3m grid bounds for Everyday Objects in foreground
GRID_MIN = -1.5
GRID_MAX = 1.5


# Get collections from Blender file
camera_collection, light_collection, ocean_collection, objects_collection = func.get_collections()

# Printing messages to terminal and asking for user confirmation
func.print_render_msg(RENDER, frame_end, BASE_SAVE_PATH, res_x, res_y, res_pct)
func.print_dataset_msg(camera_collection, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_DEEP_RANGE, CLEAR_SHALLOW_RANGE, MURKY_SHALLOW_RANGE, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX)
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
            
            # Iterate over number of random arrangements
            for arr_idx in range(1, NUM_RANDOM_ARRANGEMENTS+1):
            
                # Select either CLEAR or MURKY depths
                z_offsets = func.choose_depth_type(
                    water_type,
                    CLEAR_DEEP_RANGE,
                    CLEAR_SHALLOW_RANGE,
                    MURKY_SHALLOW_RANGE
                )

                # Iterate over Z depths
                for z in z_offsets:
                    ocean_obj.location.z = z
                    real_depth = func.blender_z_to_real_depth(z)
                    
                    # Randomly arrange objects with AABB collision avoidance
                    func.rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX)
                    
                    # Print out the current configuration settings to terminal
                    func.print_render_config(cam_obj, focal, interoc, spotlight, label, frame_name, real_depth, arr_idx)

                    # Apply optimised render settings
                    func.apply_opt_render(water_type, scene)

                    # Render the current configuration
                    if RENDER:
                        func.render_config(scene, temp_output, BASE_SAVE_PATH, cam_obj, frame_name, z, arr_idx, MURKY_SHALLOW_RANGE, CLEAR_DEEP_RANGE, CLEAR_SHALLOW_RANGE, focal=focal, interoc=interoc)


# Finished
print("\nDataset generation complete!")

