
import bpy
import random
import math
import mathutils  

ROOT_COLLECTION_NAME = "Everyday Objects"
NUM_OBJECTS = 5

GRID_MIN = -1.0
GRID_MAX = 1.0
MAX_TRIES = 100

root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
if root_col is None:
    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")


def collect_objects_recursive(collection, objects):
    objects.extend(collection.objects)
    for child in collection.children:
        collect_objects_recursive(child, objects)
all_objects = []
collect_objects_recursive(root_col, all_objects)

## --- collect all objects ---
#all_objects = []
#for subcol in root_col.children:
#    all_objects.extend(subcol.objects)

if len(all_objects) < NUM_OBJECTS:
    raise RuntimeError("Not enough objects to sample from")

# --- hide all objects ---
for obj in all_objects:
    obj.hide_render = True
    obj.hide_viewport = True

selected_objects = random.sample(all_objects, NUM_OBJECTS)

placed_objects = []  # (x, y, width, depth)

depsgraph = bpy.context.evaluated_depsgraph_get()

for obj in selected_objects:
#    obj.hide_render = False

    for _ in range(MAX_TRIES):
        # random rotation FIRST
        obj.rotation_euler.z = random.uniform(0, 2 * math.pi)

        # force evaluation so bbox reflects rotation (update to get rotation)
        eval_obj = obj.evaluated_get(depsgraph)
        
        
        # compute world-space bbox coordinates
        bbox = [eval_obj.matrix_world @ mathutils.Vector(corner)
                for corner in eval_obj.bound_box]

        x_coords = [v.x for v in bbox]
        y_coords = [v.y for v in bbox]

        width = max(x_coords) - min(x_coords)
        depth = max(y_coords) - min(y_coords)

#        # compute FULL width/depth from bounding box
#        x_coords = [v[0] for v in eval_obj.bound_box]
#        y_coords = [v[1] for v in eval_obj.bound_box]

#        width = max(x_coords) - min(x_coords)
#        depth = max(y_coords) - min(y_coords)

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
            
            obj.hide_viewport = False
            obj.hide_render = False
            
            break
    else:
        print(f"Warning: Could not place {obj.name} without overlap.")

print("Selected objects placed:")
for obj in selected_objects:
    print(" -", obj.name)






# RESET AND ENABLE VIEWPORT FOR EVERYTHING
import bpy
import random

ROOT_COLLECTION_NAME = "Everyday Objects"

root_col = bpy.data.collections.get(ROOT_COLLECTION_NAME)
if root_col is None:
    raise RuntimeError(f"Collection '{ROOT_COLLECTION_NAME}' not found")

# --- collect all objects from the sub-collections ---
all_objects = []
for subcol in root_col.children:
    all_objects.extend(subcol.objects)
    
for obj in all_objects:
    obj.hide_render = True
    obj.hide_viewport = False  # Uncomment in console if needed
    
#    obj.location.z = 0





















import bpy
import random
import math
import mathutils  

def rand_arrange_objects(arr_idx, all_objects, MIN_OBJECTS, MAX_OBJECTS, GRID_MIN, GRID_MAX, MAX_TRIES=100):
    print(f"Random arrangement {arr_idx}")

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

            if not overlap:
                # Place object
                obj.location.x = x
                obj.location.y = y
                obj.hide_render = False
                # obj.hide_viewport = False  # Uncomment for Blender viewport

                placed_objects.append((x, y, width, depth))
                objects_placed_count += 1
                break
        else:
            # Could not place this object; try next one
            print(f"Warning: Could not place {obj.name} without overlap, skipping.")

    print("Objects successfully placed:")
    for x, y, w, d in placed_objects:
        print(f" - AABB center: ({x:.2f}, {y:.2f}), size: ({w:.2f}, {d:.2f})")

