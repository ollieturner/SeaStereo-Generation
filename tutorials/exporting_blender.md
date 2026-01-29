# TUTORIAL

TO DO: 
debugging - CHANGE TO BASH SCRIPT NAMES 

## Exporting in Blender

### Aim
This tutorial explains the Blender render setup and changes the location the renders are saved to. 

### Background
The .blend file has two render output channels - the standard, global render and the custom render from the Compositing Nodes. 


The global render is an image of the scene. Its settings are in Output Properties in the Control Panel tab (bottom right). This is where raw image is generated.


The Compositing node diagram allows for more control over the renders, including different file types, the data included and the number of renders. Compositing in Blender is intended for intermediary, or differently layered renders. This is where raw depth is generated.


Note that screenshots are provided in Instructions. 



### Initial Configuration

The .blend file is currently configured to save the raw image and raw depth renders into `results/blender_output/temp/`.

The global render path can be overriden in Python but the Compositing Node render cannot. As a result, running the scripts and .blend files on a new machine will result in errors. The global renders will save correctly into the relative `results/blender_output/temp/` folder in the repo, but the Compositing Node will attempt to render to: `/home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/results/blender_output/temp/`.

Therefore, follow the instructions to change the Compositing Render path to the `results/` folder on your machine before rendering.

Also, the .gitignore will not push the `results/` folder, as this will quickly get too large to push to git when generating a dataset. Save datasets to Hugging Face instead.


### Instructions

#### Global Render - Raw Image

Change the global render output path by selecting the folder icon in this tab: 

![alt text](images/export_global.png)

This may also be overridden in Python with:

```
# Define render output path
output_path = os.path.expanduser("results/blender_output/temp/")

# Set render output
scene.render.filepath = output_path
```

See `render_animation.py` or `render_image.py` as an example. 

#### Compositing Render - Raw Depth

Change the Compositing Node output path in this tab by again selecting the folder icon. If more output types are added, then repeat for each.


![alt text](images/export_compositing.png)

Currently not sure how to override in Python. This is a point of improvement - see *Why use a temp folder?* in FAQs.



### Testing Export 


<!-- CHANGE TO BASH SCRIPTS -->

Test that exporting is working correctly by rendering a single frame - run `render_animation.py` (with scene.frame_end = 1) or `render_image.py`.  You should expect this organisation:

 
![alt text](images/test_export_path.png)


Then check the terminal to read directly where renders are outputted to. Whenever Blender renders it prints the output file's location to the terminal that opened Blender. You should expect a message similar to this in terminal, with file paths for your machine: 

<pre>Blender 5.0.1 (hash a3db93c5b259 built 2025-12-16 01:30:59)
00:01.618  blend            | Read blend: &quot;/home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender/underwater_scene.blend&quot;
00:41.476  render           | Saved: &apos;/home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/results/blender_output/temp/raw depth0001_L.exr&apos;
00:41.493  render           | Saved: &apos;/home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/results/blender_output/temp/raw depth0001_R.exr&apos;
00:41.529  render           | Saved: &apos;results/blender_output/temp/0001_L.jpg&apos;
00:41.565  render           | Saved: &apos;results/blender_output/temp/0001_R.jpg&apos;
Animation render complete

Blender quit
</pre>



### FAQs


#### *Why use a temp folder?*

When generating a dataset, each set of frames for a configuration is saved in a nested folder structure to identify its characteristics e.g. `Approach Camera/Jerlov/Arrangement 1/<images>`.

I struggled to automate this process in a Python script, where I expected to be able to index into and edit the Compositing Node outputs. So instead, I have left them to export into a temporary folder. Then, at the end of each pass, the files are moved from `temp/` into their nested folder location. Using `temp/` rather than the base `blender_output/` prevents recursive copying. 

If it is possible to override the Compositing Node output path in path, then the .blend could directly render into the desired location on each pass, rather than moving files each time. This would reduce overhead. 

#### *Why is there a normalize node?*

For inputting into the neural network for training, raw image and raw depth is required. Normalising the depth values is unnecessary information for the model. However, it is very useful for visualisation. Compare the two pictures below. 


| Raw depth | Normalised depth |
|------------------------------|----------------------------------|
| ![alt text](images/raw_depth_example.png) | ![alt text](images/normalized_depth_example.png) |


When desired, connect the 'Normalize' node to the file output node and use the following settings. 

![alt text](images/normalized_depth_settings.png)



#### *Can you disable global renders and export only from the Compositing Nodes?*

My understanding is that it is not possible to disable the global render. This is a common issue faced by other Blender users (after researching in forums). 

Hence, the .blend scene was corrected to output raw image from the global render, and raw depth from the Compositing Nodes. This removed an unnecessary, extra global render that had to be deleted on each run. 


<!-- 
Compositing in Blender is intended for intermediary, or differently layered, renders. Blender still outputs a final, complete render. For our dataset, we are not interested in this render (as it undergoes processes like colour correction) - we just want the raw image and raw depth. 


However, it is not possible to disable the global render. This is a common issue faced by other Blender users (after researching in forums). 


This setup is configured to save the undesired global renders into delete_global/. This folder is then automatically deleted in the dataset generation scripts - so after generating a dataset, the final outputs are just raw image and raw depth. It is not deleted in render_animation or render_image, so expect to see delete_global/ persist there.  -->