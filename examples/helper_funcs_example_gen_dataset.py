# Helper functions specific to generating an example dataset

# Convert blender offset to approximate real depth
def blender_z_to_real_depth(z_blender):
    return z_blender + 25

# Print example dataset characteristics to terminal before generation 
def print_example_dataset_msg(chosen_camera, FOCAL_LENGTHS, INTEROCULAR_DIST, WATER_CONDITIONS, CLEAR_Z_OFFSETS, MURKY_Z_OFFSETS, MIN_OBJECTS, MAX_OBJECTS, NUM_RANDOM_ARRANGEMENTS, GRID_MIN, GRID_MAX):
    print("---DATASET FEATURES---")

    # Print chosen camera
    print(f"Chosen camera: {chosen_camera}")

    # List available camera types
    print("Camera types:")
    print("  Focal lengths:", end=" ")
    for i, f in enumerate(FOCAL_LENGTHS):
        if i > 0:
            print(", ", end="")
        print(f"{f}mm", end="")
    print() #  newline
    print("  Interocular distances:", end=" ")
    for i, d in enumerate(INTEROCULAR_DIST):
        if i > 0:
            print(", ", end="")
        print(f"{d}mm", end="")
    print()

    # List available water conditions
    print("Water conditions:")
    for _, label, _ in WATER_CONDITIONS:
        print(f"  - {label}")

    # List available depths (in real-world, with blender offset applied)
    print("Depths (real-world):")
    clear_depths = [blender_z_to_real_depth(z) for z in CLEAR_Z_OFFSETS]
    murky_depths = [blender_z_to_real_depth(z) for z in MURKY_Z_OFFSETS]
    print(f"  Clear water depths: {clear_depths} m")
    print(f"  Murky water depths: {murky_depths} m")

    # List object configuration properties 
    print("Object placement:")
    print(f"  Objects per scene: {MIN_OBJECTS}–{MAX_OBJECTS}")
    print(f"  Random arrangements per configuration: {NUM_RANDOM_ARRANGEMENTS}")
    print(f"  Foreground grid: {GRID_MIN} m to {GRID_MAX} m (X/Y)")

# Ask the user for confirmation before proceeding with dataset generation
def get_example_confirmation():
    print("\nThis will generate an example, sample dataset")
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

# Only render for the chosen camera (skip over unchosen in loop)
def compare_camera(cam_obj, chosen_camera):
    cam_name = cam_obj.name.replace(" Camera", "").strip()
    return cam_name == chosen_camera