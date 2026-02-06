# TUTORIAL

## Saving Videos

### Aim
This tutorial explains how to convert the series of rendered RGB images into a video, for both single and stereo (L/R side-by-side) views.


### Background
It is useful for visualisation to turn the series of rendered images into a video. This can also confirm the camera is moving correctly on its path. 

The single view refers to a video from only one camera e.g. either just left camera. The stereo view refers to a video with the left and right camera feeds playing simultaneously side-by-side. 


<!-- | Single View | Stereo View |
|------------------------|-----------------------------|
|  |  | -->


The referenced scripts are contained in `scripts/misc`.

### Instructions

#### Single View
In `save_single_view_video.py`:

- Change the `base_folder` variable to the path of the folder where the images are stored. 

- Change `fps` to desired FPS

- Change the output video name with `video_name`

- Currently figured to read `image_type = "*_L.jpg"` files. Change as needed with `image_type`


Run the script as normal for Python e.g. from VS Code. It will generate the video and save it into a new `videos/` folder inside the `base_folder`. 


#### Stereo View
In `save_stereo__video.py`:

- Change the `base_folder` variable to the path of the folder where the images are stored. 

- Change `fps` to desired FPS

- Change the output video name with `video_name`

- Currently figured to read `image_type = "*_L.jpg"` files. Change as needed with `PASSES`. Can also add more file types to do multiple passes in one run.


Run the script as normal for Python e.g. from VS Code. It will generate the video and save it into a new `videos/` folder inside the `base_folder`. 


