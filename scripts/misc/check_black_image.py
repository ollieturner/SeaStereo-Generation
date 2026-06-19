# Delete this when donefrom PIL import Image
from PIL import Image

# input / output paths
input_path = "0001_L.jpg"
output_path = "output.jpg"

# open image
img = Image.open(input_path)

# ensure it's fully loaded (avoids lazy loading issues)
img.load()

# save again as jpg
img.save(output_path, format="JPEG", quality=95)