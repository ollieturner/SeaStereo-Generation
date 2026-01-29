# Simulated-Underwater-Depth-Dataset-Generation

Generation of simulated datasets containing raw image and raw depth of diverse underwater scenes with a stereo camera in Blender. Scenes include realistic seafloor environments and submerged everyday objects. Datasets will be used for training a neural network to recognise depth from an image, which is the basis for underwater grasping. 


## Table of Contents




- Add in Hugging Face (link to)
--> Explain git repo organisation earlier?
- Test scripts
- Script to run after installation to test its working (have to change output export path first?)
- Turn terminal commands into scripts
- Sample dataset
- Reference tutorials and recommended
- scripts configured to read .blend file on my machine, you will need to change the paths to wherever you store the .blend scene after downloading from Hugging Face 
- Also need to change the export paths in files 

CURRENT SETUP: 
Getting Started 
- Pulling Repo
- Blender Installation 
- Learning Blender
Repo Organisation 
Dataset Characteristics
- Outputs
- Features
- Size, Time
How to Use
- (Tutorials)
Known Issues
Notes for Improvement
Contact




## Getting Started 

### Pulling Repo

In terminal, navigate to where you want to store the repo. Then pull with: 

```
git clone https://github.com/ollieturner/Simulated-Underwater-Depth-Dataset-Generation.git
```
### Blender Installation

If not installed already, follow the Blender installation instructions [here](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 

Any version >= 4.3 is compatible (for the water conditions). Verify version with `blender --version` after installation. 

### Learning Blender

Before using the scripts and blender scenes in this repo, if you are new to Blender I recommend following a few tutorials to gain a general understanding of Blender and common controls. 





<!-- Recommend the following tutorials to gain a general understanding of using Blender and common controls. 

(cookie - particularly good for learning how to make keyframes and camera trajectory)
(camera orbit - more work on camera trajectory)
(interpolation demo? ) -->

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

Big factors in changing time is depth and water conditions 

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

<!-- left it configured to export results into results folder in git repo, but change this as needed. not uploading or tracking this folder since it is large 
blender/ in hugging face -->



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


## Notes for Improvement

Currently a subset of everyday ShapeNet objects have been manually selected, imported and organised into collections that are iterated over. This object selection and import could be automated in the dataset generation script. 


## Contact: 
<otur3695@uni.sydney.edu.au>

Oliver Turner (UG student at USYD, finishing Sem 2 2026)



<!-- Make sure there are examples on how to use  -->






<!-- 

## Dataset and Assets

Large Blender assets and generated datasets are hosted on Hugging Face:

https://huggingface.co/datasets/ollieturner/simulated-underwater-depth

Download instructions:

```bash
pip install huggingface_hub
python scripts/download_assets.py -->



<!-- # Install the Hugging Face CLI
curl -LsSf https://hf.co/cli/install.sh | bash

# (optional) Login with your Hugging Face credentials
hf auth login

# Push your dataset files
hf upload owt3/Simulated-Underwater-Depth-Dataset-Generation . --repo-type=dataset

You can also upload directly from the website using the File Uploader. -->

<!-- https://huggingface.co/datasets/owt3/Simulated-Underwater-Depth-Dataset-Generation -->
