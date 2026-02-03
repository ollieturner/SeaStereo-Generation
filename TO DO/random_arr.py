
# ## RESET AND ENABLE VIEWPORT FOR EVERYTHING
# #import bpy
# #import random

# #ROOT_COLLECTION_NAME = "Everyday Objects"

# #root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
# #if root_col is None:
# #    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# ## --- collect all objects from the sub-collections ---
# #all_objects = []
# #for subcol in root_col.children:
# #    all_objects.extend(subcol.objects)
# #    
# #for obj in all_objects:
# #    obj.hide_render = True
# #    obj.hide_viewport = False  # Uncomment in console if needed
# #    
# ##    obj.location.z = 0




# import bpy
# import random
# import math

# ROOT_COLLECTION_NAME = "Everyday Objects"
# NUM_OBJECTS = 5

# GRID_MIN = -1.5
# GRID_MAX = 1.5
# MAX_TRIES = 50
# PADDING = 0.1  # small buffer to avoid overlaps

# root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
# if root_col is None:
#     raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# # --- collect all objects from sub-collections ---
# all_objects = []
# for subcol in root_col.children:
#     all_objects.extend(subcol.objects)

# if len(all_objects) < NUM_OBJECTS:
#     raise RuntimeError("Not enough objects to sample from")

# # --- disable all objects for render ---
# for obj in all_objects:
#     obj.hide_render = True
#     obj.hide_viewport = True

# # --- randomly select objects ---
# selected_objects = random.sample(all_objects, NUM_OBJECTS)

# # --- place objects without overlap in X/Y using conservative bounding box ---
# placed_positions = []

# for obj in selected_objects:
#     # compute conservative half-width/depth ignoring rotation
#     x_coords = [abs(v[0]) * obj.scale[0] for v in obj.bound_box]
#     y_coords = [abs(v[1]) * obj.scale[1] for v in obj.bound_box]
#     half_width = max(x_coords) + PADDING
#     half_depth = max(y_coords) + PADDING

#     for _ in range(MAX_TRIES):
#         # random rotation still applied visually
#         obj.rotation_euler.z = random.uniform(0, 2 * math.pi)

#         # choose random position within grid bounds
#         x = random.uniform(GRID_MIN + half_width, GRID_MAX - half_width)
#         y = random.uniform(GRID_MIN + half_depth, GRID_MAX - half_depth)

#         # check overlap with previously placed objects
#         overlap = False
#         for px, py, pw, pd in placed_positions:
#             if (abs(x - px) < (half_width + pw)) and (abs(y - py) < (half_depth + pd)):
#                 overlap = True
#                 break

#         if not overlap:
#             obj.location.x = x
#             obj.location.y = y
#             placed_positions.append((x, y, half_width, half_depth))
#             obj.hide_render = False
#             obj.hide_viewport = False
#             break
#     else:
#         print(f"Warning: Could not place {obj.name} without overlap.")

# print("Selected objects placed:")
# for obj in selected_objects:
#     print(" -", obj.name)




# # MOST RECENT
# #import bpy
# #import random
# #import math

# #ROOT_COLLECTION_NAME = "Everyday Objects"
# #NUM_OBJECTS = 5

# #GRID_MIN = -1.5
# #GRID_MAX = 1.5
# #MAX_TRIES = 50
# #PADDING = 0.1 # 0.01

# #root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
# #if root_col is None:
# #    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# ## collect objects
# #all_objects = []
# #for subcol in root_col.children:
# #    all_objects.extend(subcol.objects)

# #if len(all_objects) < NUM_OBJECTS:
# #    raise RuntimeError("Not enough objects to sample from")

# #for obj in all_objects:
# #    obj.hide_render = True
# #    obj.hide_viewport = True

# #selected_objects = random.sample(all_objects, NUM_OBJECTS)

# #placed_positions = []

# #for obj in selected_objects:
# #    for _ in range(MAX_TRIES):
# #        # choose random rotation first
# #        rot = random.uniform(0, 2*math.pi)
# #        obj.rotation_euler.z = rot

# #        # compute conservative half-width/depth after rotation
# #        x_coords = [v[0] * obj.scale[0] for v in obj.bound_box]
# #        y_coords = [v[1] * obj.scale[1] for v in obj.bound_box]

# #        # rotate each corner around Z
# #        rotated_x = [x * math.cos(rot) - y * math.sin(rot) for x, y in zip(x_coords, y_coords)]
# #        rotated_y = [x * math.sin(rot) + y * math.cos(rot) for x, y in zip(x_coords, y_coords)]

# #        half_width = (max(rotated_x) - min(rotated_x)) / 2 + PADDING
# #        half_depth = (max(rotated_y) - min(rotated_y)) / 2 + PADDING

# #        # choose random position
# #        x = random.uniform(GRID_MIN + half_width, GRID_MAX - half_width)
# #        y = random.uniform(GRID_MIN + half_depth, GRID_MAX - half_depth)

# #        # check overlap
# #        overlap = False
# #        for px, py, pw, pd in placed_positions:
# #            if (abs(x - px) < (half_width + pw)) and (abs(y - py) < (half_depth + pd)):
# #                overlap = True
# #                break

# #        if not overlap:
# #            obj.location.x = x
# #            obj.location.y = y
# #            placed_positions.append((x, y, half_width, half_depth))
# #            obj.hide_render = False
# #            obj.hide_viewport = False
# #            break
# #    else:
# #        print(f"Warning: Could not place {obj.name} without overlap.")

# #print("Selected objects placed:")
# #for obj in selected_objects:
# #    print(" -", obj.name)












# Issues 
# Change from half width to full width
# Do random rotation before checking overlap 
# Or just remove random rotation 


# VERIFIED WORKING 
import bpy
import random

ROOT_COLLECTION_NAME = "Everyday Objects"
NUM_OBJECTS = 3

GRID_MIN = -1.0
GRID_MAX = 1.0
MAX_TRIES = 100  # max attempts to place without overlap

root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
if root_col is None:
    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# --- collect all objects from the sub-collections ---
all_objects = []
for subcol in root_col.children:
    all_objects.extend(subcol.objects)

if len(all_objects) < NUM_OBJECTS:
    raise RuntimeError("Not enough objects to sample from")

# --- disable all objects for render ---
for obj in all_objects:
    obj.hide_render = True

# --- randomly select objects ---
selected_objects = random.sample(all_objects, NUM_OBJECTS)

# --- place objects without overlap ---
placed_positions = []

for obj in selected_objects:
    obj.hide_render = False

    # bounding box half extents
    x_coords = [v[0] for v in obj.bound_box]
    y_coords = [v[1] for v in obj.bound_box]
    half_width = (max(x_coords) - min(x_coords)) / 2
    half_depth = (max(y_coords) - min(y_coords)) / 2

    for _ in range(MAX_TRIES):
        x = random.uniform(GRID_MIN + half_width, GRID_MAX - half_width)
        y = random.uniform(GRID_MIN + half_depth, GRID_MAX - half_depth)

        # check overlap
        overlap = False
        for px, py, pw, pd in placed_positions:
            if (abs(x - px) < (half_width + pw)) and (abs(y - py) < (half_depth + pd)):
                overlap = True
                break

        if not overlap:
            obj.location.x = x
            obj.location.y = y
            obj.rotation_euler.z = random.uniform(0, 6.28318)
            placed_positions.append((x, y, half_width, half_depth))
            break
    else:
        print(f"Warning: Could not place {obj.name} without overlap.")

print("Selected objects placed:")
for obj in selected_objects:
    print(" -", obj.name)










## TO TEST 
# FULL WIDTH AABB + ROTATION-AWARE
# inpisred by https://www.youtube.com/watch?v=bFURdsszto0
import bpy
import random
import math

ROOT_COLLECTION_NAME = "Everyday Objects"
NUM_OBJECTS = 3

GRID_MIN = -1.0
GRID_MAX = 1.0
MAX_TRIES = 100

root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
if root_col is None:
    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# --- collect all objects ---
all_objects = []
for subcol in root_col.children:
    all_objects.extend(subcol.objects)

if len(all_objects) < NUM_OBJECTS:
    raise RuntimeError("Not enough objects to sample from")

# --- hide all objects ---
for obj in all_objects:
    obj.hide_render = True

selected_objects = random.sample(all_objects, NUM_OBJECTS)

placed_objects = []  # (x, y, width, depth)

depsgraph = bpy.context.evaluated_depsgraph_get()

for obj in selected_objects:
    obj.hide_render = False

    for _ in range(MAX_TRIES):
        # random rotation FIRST
        obj.rotation_euler.z = random.uniform(0, 2 * math.pi)

        # force evaluation so bbox reflects rotation (update to get rotation)
        eval_obj = obj.evaluated_get(depsgraph)

        # compute FULL width/depth from bounding box
        x_coords = [v[0] for v in eval_obj.bound_box]
        y_coords = [v[1] for v in eval_obj.bound_box]

        width = max(x_coords) - min(x_coords)
        depth = max(y_coords) - min(y_coords)

        x = random.uniform(GRID_MIN + width / 2, GRID_MAX - width / 2)
        y = random.uniform(GRID_MIN + depth / 2, GRID_MAX - depth / 2)

        overlap = False
        for px, py, pw, pd in placed_objects:
            # FULL WIDTH AABB (TokyoEdtech style)
            x_collision = abs(x - px) * 2 < (width + pw)
            y_collision = abs(y - py) * 2 < (depth + pd)

            if x_collision and y_collision:
                overlap = True
                break

        if not overlap:
            obj.location.x = x
            obj.location.y = y
            placed_objects.append((x, y, width, depth))
            break
    else:
        print(f"Warning: Could not place {obj.name} without overlap.")

print("Selected objects placed:")
for obj in selected_objects:
    print(" -", obj.name)
