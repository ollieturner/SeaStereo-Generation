
# # blender -b blender_scene/underwater_scene.blend --python scripts/misc/debug_black_render.py

import bpy

light_collection = bpy.data.collections.get("Camera Lights")
print("--- Light collection hide flags ---")
print("Collection hide_render:", light_collection.hide_render)
print("Collection hide_viewport:", light_collection.hide_viewport)

for obj in light_collection.objects:
    print(f"{obj.name!r}: hide_render={obj.hide_render}, hide_viewport={obj.hide_viewport}, "
          f"visible_get={obj.visible_get()}, power={obj.data.energy}")

# Check view layer level exclusion too
vl = bpy.context.view_layer
def walk(lc, depth=0):
    print("  "*depth, lc.name, "exclude=", lc.exclude)
    for c in lc.children:
        walk(c, depth+1)
walk(vl.layer_collection)




# Printing out availoable cameras and lights
# import bpy

# camera_collection = bpy.data.collections.get("Cameras")
# light_collection = bpy.data.collections.get("Camera Lights")

# print("--- Cameras ---")
# for obj in camera_collection.objects:
#     print(repr(obj.name))

# print("--- Lights ---")
# for obj in light_collection.objects:
#     print(repr(obj.name))