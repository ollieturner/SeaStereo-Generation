# from PIL import Image

# img_path = "scripts/misc/disparity_results/app_jerlov_IB_f25_i004_shallow/0010_L.jpg"

# # Open the image
# img = Image.open(img_path) 

# # Save as PDF
# img.save("scripts/misc/disparity_results/app_jerlov_IB_f25_i004_shallow/0010_L.pdf")



from PIL import Image
import os
import glob

# ---- Input folder ----
input_folder = "scripts/misc/disparity_results/for_diagram"


# ---- Output folder ----
folder_name = os.path.basename(input_folder)  # e.g., app_jerlov_IB_f25_i004_shallow
output_folder = os.path.join("for_diagram", folder_name)
os.makedirs(output_folder, exist_ok=True)  # create folder if it doesn't exist

# ---- Find all matching files ----
patterns = ["*_L.jpg", "*_R.jpg", "*_disparity_vis.png"]
files_to_convert = []
for pattern in patterns:
    files_to_convert.extend(glob.glob(os.path.join(input_folder, pattern)))

# ---- Convert each image to PDF ----
for input_path in files_to_convert:
    filename = os.path.basename(input_path)
    output_filename = os.path.splitext(filename)[0] + ".pdf"
    output_path = os.path.join(output_folder, output_filename)
    
    img = Image.open(input_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img.save(output_path)
    print(f"Saved {output_path}")