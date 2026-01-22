# Simulated-Underwater-Depth-Dataset-Generation

Generation of simulated datasets containing raw image and raw depth of diverse underwater scenes with a stereo camera in Blender. Scenes include realistic seafloor environments and submerged everyday objects. Datasets to be used for training a neural network to recognise depth from an image, which forms the basis for underwater grasping. 


## Getting Started 

### Pulling Repo

In terminal, navigate to where you want to store the repo. Then pull with: 

```
git clone https://github.com/ollieturner/Simulated-Underwater-Depth-Dataset-Generation.git
```
### Blender Installation

The NiN in J04 has Blender 5.0.1 already installed. If needed elsewhere, follow Blender installation instructions [here](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 

Any version >= 4.3 is compatible (for the water conditions). Verify version with `blender --version` after installation. 

### Learning Blender

Recommend the following tutorials to gain a general understanding of using Blender and common controls. 

(cookie - particularly good for learning how to make keyframes and camera trajectory)
(camera orbit - more work on camera trajectory)
(interpolation demo? )

<!-- ### ShapeNet
TODO: Check about ShapeNet - have to link the repo? Recommend making an accout in Installation?  -->



<!-- ### FIRST: Configuring Output Path -->

<!-- Have to change in scripts and also in blender file, add in screenshots 
suggest not saving into repo for size constraints, depending on size can upload/backup into hugging face (up to 100GB)
-->


## Repo Organisation 

<!-- move blender scenes into hugging face?? depends how big the file ends up being  -->

| Folder          | Description                                                                                                     |
|-----------------|-----------------------------------------------------------------------------------------------------------------|
| blender_scenes  | Blender files for underwater environments                                                                       |
| ShapeNet TODO   | Everyday object models to use in underwater scenes from ShapeNet/Link to ShapeNet repo TODO                     |
| scripts/blender | Python scripts to run blender processes automated and in the background e.g. changing configurations, rendering |
| scripts/misc    | Other miscellaneous but relevant python scripts                                                                 |
| demos           | Results to demonstrate scripts, with sub-folders for each script                                                |

<!-- Table generated with: https://www.tablesgenerator.com/markdown_tables# -->

<!-- TODO: Link to Hugging Face for demo results? Or add in a suggestion to use that?  -->



## Dataset Characteristics

### Outputs

The dataset contains raw images (.jpg) and raw depth (.exr), each for left and right camera - one frame from Blender outputs 4 images. 

Each render is 240 frames (10s at 24 FPS). This is the current configuration; the number of frames is easily adjustable. <!-- TODO LINK TO HOW TO? -->

An example of the folder organisation is provided below. 

<!-- INSERT SCREENSHOT  -->

### Features

The repo is configured to iterate over combinations (think nested for loops) with the following features: 

<!-- TODO 
- Environment
    - No Background 
    - Rocky background (?) 
- Lighting 
    - Spotlight (dark)
    - Spotlight (med)
    - Spotlight (bright)
    - Caustic
- Depth 
- Camera parameters
- Water conditions (all with marine snow) (Jerlovs)
- Objects (lone, multiple, rocks, everyday)
- Camera trajectories
    - Orbit
    - Linear approach 
    - Arc approach
    - Arc approach and retreat
    - Sweeps (?)  -->

See 'demos/dataset_summary' to see example photo and videos for the above features. <!-- OR LINK TO HUGGING FACE? --> 

<!-- Desired features can be selected/removed, as explained in TODO -->

State number of things in a table? For diversity? - then number of combinations? 

### Size, Time

<!-- TODO -->
<!-- put into table? -->

Rendering of one frame (4 output images) takes INSERT TIME and is INSERT SIZE. 

For a complete render of a feature (240 frames) this takes **INSERT TIME** and is **INSERT SIZE**. 

Over all INSERT NUMBER features, there are INSERT NUMBER COMBS. This will take **INSERT TIME** and is **INSERT SIZE**. 
<!-- Rephrase this if making a table of combinations  -->

In total, there will be INSERT NUMBER of raw image and raw depth pairs. 


## How to Use 

<!-- ### FIRST: Configuring Output Path

Have to change in scripts and also in blender file, add in screenshots 

or a note on making sure you have done this previously 
suggest not saving into repo for size constraints, depending on size can upload/backup into hugging face (up to 100GB)

-->



### Generate Dataset  
<!-- Script to run automated dataset process
- Note how number of frames can be adjusted
- Note on how to select features 
- Check if they want a full combinatorics nested for loops -->


### Render Animation 

<!-- emphasis single animation  -->

### Render Single Image 
<!-- - provide script or just set num of frames to 1 -->
<!-- emphasis single animation  -->


### Converting Images to Video
<!-- useful for visualising camera trajectories empirically/qualitatively  -->

<!-- single view
stereo 
(different files or make option in the same file?) -->

### Check Depth 



## How to Add Components 

<!-- Describing adding into blender manually 
then configured in python scripts
- since easier to visualise and confirm changes, and GUI is intuitive and just much easier

link useful tutorials 

use things as inspiration, copy from a base and build/experiment from there  -->



## Known Issues

<!-- Note on bug that still does global render, link that it is a current/ongoing issue  -->


## Contact: 
<otur3695@uni.sydney.edu.au>

Oliver Turner (UG student at USYD, finishing Sem 2 2026)



<!-- Make sure there are examples on how to use  -->


