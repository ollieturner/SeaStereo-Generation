# NOT A FOCUS SINCE NOT STEREO

# Save rendered animation images as a video
# For single view (just testing)

import cv2
import glob
import os

folder = "/home/otur3695/Documents/Blender/automate_test/blender_anim"

frames = sorted(glob.glob(os.path.join(folder, "00*.png")))

print(f"Found {len(frames)} frames")

if len(frames) == 0:
    raise RuntimeError("No frames found")

fps = 2

# Read first frame to get size
img = cv2.imread(frames[0])
h, w, _ = img.shape
out_size = (w, h)

# Video writer
out_path = os.path.join(folder, "cookie_anim.mp4")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(out_path, fourcc, fps, out_size)

for fname in frames:
    img = cv2.imread(fname)
    if img is None:
        continue

    # Uncomment if TIF looks too dark
    # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")

    writer.write(img)          # save frame
    cv2.imshow("Playback", img)

    if cv2.waitKey(int(1000 / fps)) & 0xFF == 27:
        break

writer.release()
cv2.destroyAllWindows()

print(f"Saved video to: {out_path}")
