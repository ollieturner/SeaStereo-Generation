# Simulated-Underwater-Depth-Dataset-Generation

Generation of simulated datasets containing raw RGB and depth images of diverse underwater scenes with a stereo camera in Blender. Scenes include realistic seafloor environments and submerged everyday objects. Datasets will be used for training a neural network to recognise depth from an image, which is the basis for underwater grasping.




| Clear, shallow water | Clear, deep water | Murky, shallow water |
|----|----|----|
|  ![alt text](tutorials/images/arc_clear.jpg) |  ![alt text](tutorials/images/clear_deep.jpg) |  ![alt text](tutorials/images/murky_shallow.jpg) |


The dataset, in terms of its size and diversity, is **customisable**. The current setup produces a dataset with 260 configurations with 5 camera paths, 4 camera types, 8 water conditions in 1-2 depths. With 30 rendered frames for each configuration, the complete dataset will be **14.34 GB** and take **10 days, 2 hours** to generate on our tested computer. In total, there would be **7,800** raw RGB and depth pairs.

The repository and Blender scenes were developed and rendered using Blender 5.0.1 on Ubuntu 24.04, with two NVIDIA GeForce RTX 3080 Ti GPUs.



## Table of Contents


1. [Getting Started](#getting-started)
   * [Pulling the Repository](#pulling-the-repository)
   * [Downloading the Hugging Face Dataset](#downloading-the-hugging-face-dataset)
   * [Blender Installation](#blender-installation)
   * [Downloading ShapeNetCore](#downloading-shapenetcore)
   * [First Steps](#first-steps)
2. [Repository Organisation](#repository-organisation)
3. [Dataset Characteristics](#dataset-characteristics)
4. [Testing with Examples](#testing-with-examples)
5. [How to Use](#how-to-use)
6. [Notes for Improvement](#notes-for-improvement)
7. [Contact](#contact)
8. [References](#references)


## Getting Started

### Pulling the Repository

In a terminal, navigate to where you want to store the repository. Then pull with:

```
git clone https://github.com/ollieturner/Simulated-Underwater-Depth-Dataset-Generation.git
```

Then check the pull worked correctly with:

``` 
cd Simulated-Underwater-Depth-Dataset-Generation
git status 
```

Check the repository's contents with `ls` when inside.



### Downloading the Hugging Face Dataset

The Blender scene, background objects and everyday/foreground objects are stored in a Hugging Face dataset due to storage requirements.

First, if you don't have a Hugging Face account already, make one [here](https://huggingface.co/).

Download the Hugging Face dataset from [here](https://huggingface.co/datasets/owt3/Simulated-Underwater-Depth-Dataset-Generation/tree/main).

<!-- EDIT/CHECK THIS -->

After downloading, move everything into the `blender_scene/` in your local version of this repository. This ensures the referenced relative paths operate correctly - in particular, renders call the Blender file in the `blender_scene/` folder. The .gitignore will leave these folders untracked, as they are too big to push to GitHub.


<!-- Move the ShapeNet object folders (e.g. bench_*, bin_*) into a ShapeNet_objects subfolder inside `everyday objects/`. Then move each of the folders into `blender_scene/` in your local version of this repository. This ensures the referenced relative paths operate correctly - in particular, renders call the Blender file in the `blender_scene/` folder. The .gitignore will leave these folders untracked, as they are too big to push to GitHub.

The expected organisation of the local repository is explained in [Repository Organisation](#repository-organisation). -->





### Blender Installation

If not installed already, follow the Blender installation instructions [here](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html).

Any version >= 4.3 is compatible (for the water conditions). Verify version with `blender --version` after installation.

#### Learning Blender

If you are new to Blender, I recommend following this [tutorial](https://www.youtube.com/watch?v=Ci3Has4L5W4). This will give a general understanding of common controls.


### Downloading ShapeNetCore

The objects of interest in the foreground are sourced from [ShapeNet](https://shapenet.org/). Selected objects are already downloaded and included in the aforementioned Hugging Face dataset. These include benches, couches, chairs and mugs.

If you'd like more ShapeNet objects, make a ShapeNet account and follow their instructions to download ShapeNetCore from their Hugging Face. Note that these two steps require an approval from ShapeNet, so allow a day for each of the approvals. See `tutorials/importing_objects` for further detail on adding objects.


### First Steps

I first advise reading the rest of this README to understand the dataset and how to change its contents.

Once you begin rendering, either from the automated Python scripts or directly from the Blender file, you will need to change the output paths in the Blender file to your local machine. See `tutorials/exporting_blender` for further detail and instructions.


## Repository Organisation



| Folder | Description |
|----|----|
| blender_scene | Blender files for underwater environments, including scene, objects and sand (from HF) |
| examples | Contains example scripts in scripts/ and expected results to compare with in results/ |
| results | Empty folder to that Blender scene outputs into. Its contents are not tracked to avoid pushing large datasets |
| scripts/blender | Python scripts to run automated Blender processes e.g. generating dataset, rendering images |
| scripts/misc | Other Python scripts e.g. saving a video from rendered images |
| tutorials | Guided tutorials on using the Blender scene file e.g. adding cameras and objects |


Note HF denotes folders from the Hugging Face dataset. They are ignored by the .gitignore and will not be tracked by the repository.

<!-- Table generated with: https://www.tablesgenerator.com/markdown_tables# -->


## Dataset Characteristics

The **features types and quantities are customisable**. They can be edited either in the Blender scene or the automated Python script (see [Changing the Dataset](#changing-the-dataset)). The current setup (260 configurations) is shown below.

| **Camera Paths** | **Camera Types** | **Water Conditions** | **Depths** | **Random Arrangements** |
|----|----|----|----|----|
| Approach and retreat<br>Arc <br>Horizontal pan<br>Orbit <br>Top-view pan | Low focal length (1.5mm), low interocular (0.04mm)<br>High focal length (2.5mm), high interocular (0.08mm)<br>Low focal length, high interocular<br>High focal length, low interocular | Clear: <br>- Jerlov<br>- Jerlov IA<br>- Jerlov IB<br>- Jerlov II<br>- Jerlov IC<br><br>Murky: <br>- Jerlov III<br>- Jerlov 5C<br>- Jerlov 3C | Clear:<br>- 5m<br>- 20m <br><br>Murky:<br>- 2m | 1 random arrangement |

With an image width of 640 pixels and sensor width of 6.7mm, the low and high focal lengths may also be expressed as 143 and 239 pixel units, respectively.

The dataset produces raw RGB and depth images (.jpg, .exr respectively). With a left and right camera for the stereo setup, this means one rendered frame of the scene outputs 4 images.

One rendered frame (4 images) is \~1.8 MB. The time for one render is \~1-2mins - this value varies with each configuration, and mostly depends on water condition and depth (clear/shallow is fast, whilst murky/deep is slow). The resolution is set to 640x480.

With 30 rendered frames for each configuration, the complete dataset will be **14.34 GB** and take **10 days, 2 hours** to generate. In total, there would be **7,800** raw RGB and depth pairs.

An example of the folder organisation after the dataset is generated is provided below. Each render is indexed by its configuration settings.

 ![alt text](tutorials/images/dataset_characteristics_org.png)

The file organisation extends similarly for successive cameras and renders.


## Testing with Examples

### Cycling through Configurations

This example will cycle through all the dataset's configurations without rendering any images.

Each configuration will be printed to the terminal, with no images or folders generated. This will be the same process as when the dataset is generated, as this example simply sets `RENDER = False`.

From the root of this repo (`cd Simulated-Underwater-Depth-Dataset-Generation`), run `examples/example_print_configs.py` with:

```
blender -b blender_scene/underwater_scene.blend --python examples/example_print_configs.py
```

You should expect an output like this in the terminal:

<pre>Blender 5.0.1 (hash a3db93c5b259 built 2025-12-16 01:30:59)
00:01.549  blend            | Read blend: "/home/otur3695/Documents/Simulated-Underwater-Depth-Dataset-Generation/blender_scene/underwater_scene.blend"
DATASET GENERATION FOR SIMULATED UNDERWATER SCENES

\---RENDER PROPERTIES---
Rendering enabled: False
Number of frames per configuration: 1
Renders will save into: results/blender_output/
Render resolution: 640 x 480
Resolution percentage: 100%

\---DATASET FEATURES---
Available cameras:

* Approach_Retreat Camera
* Arc Camera
* Orbit Camera
* Horizontal_Pan Camera
* Top_View_Pan Camera
  Camera types:
  Focal lengths: 1.5mm, 2.5mm
  Interocular distances: 0.04mm, 0.08mm
  Water conditions:
* Jerlov I
* Jerlov IA
* Jerlov IB
* Jerlov II
* Jerlov IC
* Jerlov III
* Jerlov 5C
* Jerlov 3C
  Depths (real-world):
  Clear water depths: \[5, 20\] m
  Murky water depths: \[2\] m
  Object placement:
  Objects per scene: 3–5
  Random arrangements per configuration: 1
  Foreground grid: -1.5 m to 1.5 m (X/Y)

With the current settings, this will take \~10 days, 2 hours to render
and use \~14.34 GB of storage.
Use Ctrl+C to cancel at any time.

Proceed with dataset generation? (y/n): y
Confirmed. Starting dataset generation

Use Ctrl+C to cancel at anytime


Render with:
Approach_Retreat Camera
Focal length: 1.5mm
Interocular distance: 0.04mm
Enabled light: Clear Approach_Retreat Spot
Water condition: Jerlov I (Jerlov)
Ocean volume depth: 5 m
Random arrangement: 1
</pre>



This is a useful troubleshooting step to run to check the configurations are loading correctly, instead of rendering and reaching potential issues after hours/days.



### Generating Example Dataset

Now to finally render images! This example will render two example configurations with 30 frames each. It is currently set to render one scene in shallow, clear water, and another in shallow, murky water.

If this is your first time rendering underwater_scene.blend then you need to **change the output paths before continuing**. Otherwise you'll hit errors. See `tutorials/exporting_blender` for further detail and instructions.

From the root of this repo (`cd Simulated-Underwater-Depth-Dataset-Generation`), run `scripts/examples/example_generate_dataset.py` with:

```
blender -b blender_scene/underwater_scene.blend --python examples/example_generate_dataset.py
```

An example dataset with only 1 rendered frame per configuration is provided in `examples/eample_dataset`. You should expect scenes that resemble this:

| Clear, shallow water | Murky, shallow water |
|----|----|
|  ![alt text](tutorials/images/clear_shallow_example.jpg) |  ![alt text](tutorials/images/murky_shallow_example.jpg) |


Feel free to change the features used in the script `examples/example_generate_dataset`. This may be a useful troubleshooting step to check particular configurations without rendering a complete dataset.




## How to Use

The following sections detail how to generate and change the dataset, with tutorials referenced as needed.

Other useful tutorials in `tutorials/` involve rendering a single image/animation of the current Blender scene, converting rendered images into a video and checking the depth from .exr files.

As stated previously, please change the output path for the renders if this is your first time using underwater_scene.blend on a new machine. See `tutorials/exporting_blender` for further detail and instructions.


### Generate the Dataset

Run the following to generate the dataset. This process is predicted to use 14.34 GB of storage, and take \~10 days, 2 hours on our machine (time will vary with different computers/GPUs).

```
cd Simulated-Underwater-Depth-Dataset-Generation

blender -b blender_scene/underwater_scene.blend --python scripts/blender/generate_dataset.py
```

The number of frames per configuration is 30. This may be changed in `blender/generate_dataset.py` with the `frame_end` variable.

The features used can be customised (edited, added, removed). See the next section.


### Changing the Dataset



| Feature | How To Customise |
|----|----|
| Camera path | Follow `tutorials/adding_camera_and_water` for adding camera (and accompanying spotlight). |
| Camera type | Blender:<br>- In object settings with camera selected.<br>Python: <br>- Change focal lengths and interocular distances used with `FOCAL_LENGTHS` and `INTEROCULAR_DIST` |
| Water condition | Blender: <br>- Shader Editor of Ocean Volume object. Link the nodes as shown. (For visualising changes when editing scene) <br>Python: <br>- Change the water conditions used in `WATER_CONDITIONS` list. (For changing dataset)<br><br>See `tutorials/adding_camera_and_water` for more information |
| Depth | Blender:<br>- Z height for Ocean Volume object (offset of -25m in Blender = 0 depth) <br>Python: <br>- Change the depths used for clear and murky water in `CLEAR_Z_OFFSETS` and `MURKY_Z_OFFSETS` lists in Python |
| Random arrangement | Python:<br>- Change number of arrangements with `NUM_RANDOM_ARRANGEMENTS` variable in Python.<br>- Change the number of possible objects with `MIN_OBJECTS`, `MAX_OBJECTS`<br>- Collision avoidance is achieved with Axis-Aligned Bounding Box method in rand_arrange_objects() function. |
| Objects | Follow `tutorials/importing_objects` for adding background and foreground objects. |

## Notes for Improvement

Currently a subset of everyday ShapeNet objects have been manually selected, imported and organised into collections that are iterated over. This object import could be automated in the dataset generation script, where objects stored in the ShapeNet folder are called on each iteration.


Further work could be done on determining if it is possible to change the output render path for exports from the Compositing nodes. From my research I wasn't able to find a method that worked. This would ease the onboarding process if it is possible.


Marine snow is currently disabled, however the object is in the Ocean Collection in the Blender scene and can be enabled for render.

Underwater caustic lighting may be added. There are a number of video tutorials that can guide you through this.

## Contact:

Oliver Turner (Undergraduate student at USYD, finishing Sem 2 2026)

Email: [otur3695@uni.sydney.edu.au](mailto:otur3695@uni.sydney.edu.au)

LinkedIn: [here](www.linkedin.com/in/oliver-turner-635254291)


## References

A. X. Chang, T. Funkhouser, L. Guibas, P. Hanrahan,
Q. Huang, Z. Li, S. Savarese, M. Savva, S. Song, H. Su,
J. Xiao, L. Yi, and F. Yu. ShapeNet: An Information-Rich
3D Model Repository. Technical Report arXiv:1512.03012
\[cs.GR\], Stanford University — Princeton University —
Toyota Technological Institute at Chicago, 2015.