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
SAVE_SHAPENET_OBJS = False  # ONLY True once

SHAPENET_TXT = "shapenet_paths.txt"

func.precompute_shapenet_paths(
    "blender_scene/everyday objects/ShapeNet_objects",
    SHAPENET_TXT
)
print("Precompute complete. Set SAVE_SHAPENET_OBJS=False and rerun.")
sys.exit()

