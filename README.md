# Simulated-Underwater-Depth-Dataset-Generation

Generation of simulated datasets containing raw image and raw depth of diverse underwater scenes with a stereo camera in Blender. Scenes include realistic seafloor environments and submerged everyday objects. Datasets will be used for training a neural network to recognise depth from an image, which is the basis for underwater grasping. 



| Clear, shallow water | Clear, deep water | Murky, shallow water |
|----------------------|------------------------|-----------------------------|
| ![alt text](tutorials/images/arc_clear.jpg) | ![alt text](tutorials\images\clear_deep.jpg) | ![alt text](tutorials\images\murky_shallow.jpg) |


<!-- VIDEO NOT WORKING?  -->

<!-- | Arc camera path in shallow, clear water |
|------------------------------|
| <video controls src="tutorials\images\arc_demo.mp4" title="Title"></video> |


<video src="tutorials\images\arc_demo.mp4" placeholder="tutorials\images\arc_demo.mp4" autoplay loop controls muted title="Arc Approach Video">
Sorry, your browser doesn't support HTML 5 video.
</video> -->

<!-- <video controls src="arc_demo.mp4" title="Title"></video>  -->
<!-- <video controls src="tutorials\images\arc_demo.mp4" title="Title"></video> -->

 

## PLAN
Getting Started
--> Say what ubuntu etc it has been run on, blender version, GPUs
- Pulling Repo 
- Hugging Face 
--> Link Hugging Face (download blender folder then move into here, git ignore won't push it, but need it for relative paths in bash scripts. otherwise change paths in bash script)
- Blender Installation 
--> link cookie tutorial as beginner learning 
- Downloading ShapeNet
--> Has a subset of ShapeNet objects, to add more need to make an account 

Repo Organisation 
--> Link Hugging Face (download blender folder then move into here, git ignore won't push it, but need it for relative paths in bash scripts. otherwise change paths in bash script)
--> Add a scripts folder, fix so folders are pushed but not contents 

Dataset Characteristics 
--> Outputs
--> Features table with time
--> Predicted time and size 

Test with Sample Dataset
- Test scripts, sample dataset --> 1 for each?, a few frames in one
--> Change export path

How to use
- List out tutorials 
- Link additional useful 

Notes for Improvement
--> Include any known issues

Contact
--> Email, LinkedIn
--> Poster 

References
- ShapeNet


<!-- 
- Add in Hugging Face (link to)
-- Explain git repo organisation earlier?
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
Contact -->


## TODO
- Hugging Face organisation
- Hugging Face filepaths 
- test dataset script with render disabled
- test sample dataset with render enabled
-- do a few complete ones 



## Table of Contents

1. [Getting Started](#getting-started)
   - [Pulling the Repository](#pulling-the-repository)
   - [Pulling the Hugging Face Dataset](#pulling-the-hugging-face-dataset)
   - [Blender Installation](#blender-installation)
   - [Downloading ShapeNetCore](#downloading-shapenetcore)

2. [Repository Organisation](#repository-organisation)

3. [Dataset Characteristics](#dataset-characteristics)

4. [Testing with a Sample Dataset](#testing-with-a-sample-dataset)

5. [How to Use](#how-to-use)

6. [Notes for Improvement](#notes-for-improvement)

7. [Contact](#contact)

8. [References](#references)


## Getting Started 

The repository and Blender scenes have been used and rendered on Ubuntu 24.04, Blender 5.0.1
INSERT GPUS

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


### Pulling the Hugging Face Dataset
The Blender scene, background objects, foreground objects and sample datasets are stored in a Hugging Face dataset due to storage requirements. 

First, if you don't have a Hugging Face account already, make one [here](https://huggingface.co/).

It is important to run the following whilst inside the repository so the relative paths work correctly. Download the Hugging Face dataset:

```
huggingface-cli login
```
(CHECK IF NEEDED)

```
huggingface-cli download owt3/Simulated-Underwater-Depth-Dataset-Generation --repo-type dataset
```

Make a folder to store the Hugging Face files (not trakced by .gitignore)
```
mkdir -p blender
```
RENAME FOLDER

OR 
```
huggingface-cli download \
  owt3/Simulated-Underwater-Depth-Dataset-Generation \
  --repo-type dataset \
  --local-dir ./ \
  --local-dir-use-symlinks False

```
Then check the download worked correctly with:
```
ls datasets/Simulated-Underwater
```
CHANGE FILE PATHS/NAMES
MAKE IT DOWNLOAD INTO blender/
WILL THIS SAVE ONE FOLDER THEN HAVE IT NESTED IN THERE, CHANGE NAMES TO BE CLEARER? 


### Blender Installation

If not installed already, follow the Blender installation instructions [here](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 

Any version >= 4.3 is compatible (for the water conditions). Verify version with `blender --version` after installation. 

#### Learning Blender

Before using the scripts and scenes in this repository, if you are new to Blender I recommend following this tutorial ([here](https://www.youtube.com/watch?v=Ci3Has4L5W4)) to gain a general understanding of common controls. 


### Downloading ShapeNetCore
The objects of interest in the foreground are sourced from [ShapeNet](https://shapenet.org/). Select categories of objects are already downloaded and included in the previous Hugging Face dataset. These include benches, couches, bottles, bins, mugs and watercraft. 

If you'd like more ShapeNet objects, make a ShapeNet account and follow their instructions to download ShapeNetCore from their Hugging Face. Note that these two steps require an approval from ShapeNet, so allow a day for each of the approvals. 


<!-- ### FIRST: Configuring Output Path -->

<!-- Have to change in scripts and also in blender file, add in screenshots 
suggest not saving into repo for size constraints, depending on size can upload/backup into hugging face (up to 100GB)
-->



## Repository Organisation 

<!-- move blender scenes into hugging face?? depends how big the file ends up being  -->

| Folder          | Description                                                                                                     |
|-----------------|-----------------------------------------------------------------------------------------------------------------|
| blender         | Blender files for underwater environments, including scene, objects and sand (from HF)                          |
| demos           | Results to demonstrate scripts, with sub-folders for each script                                                |
| example_sample_dataset | An example sample dataset to compare with (from HF)                                                      |
| results         | Empty folder to that Blender scene outputs into. Its contents are not tracked to avoid pushing large datasets   |
| scripts/blender | Python scripts to run automated Blender processes e.g. generating dataset, rendering images                     |
| scripts/misc    | Other Python scripts e.g. saving a video from rendered images                                                   |
| tutorials       | Guided tutorials on using the Blender scene file e.g. adding cameras and objects                                |

Note HF denotes folders from the Hugging Face dataset. They are ignored by the .gitignore and will not be tracked by the repository. 

CHECK IF SHAPENET IN BLENDER OR OWN 

<!-- Table generated with: https://www.tablesgenerator.com/markdown_tables# -->


## Dataset Characteristics

The dataset produces raw RGB and depth images (.jpg, .exr respectively). With a left and right camera for the stereo setup, this means one rendered frame of the scene outputs 4 images. 

There are INSERT configurations. The features that are iterated over are listed below. 

INSERT TABLE 
bold headings and list underneath 

4 camera types
6 camera paths
8 water conditions 
2-3 depths (2 for murky, 3 for clear)
3 random arranegments


One rendered frame (4 images) is INSERT MB. The time for one render varies, largely with water condition and depth. See this table LINK for a breakdown of the times. The resolution is set to 640x480 - as expected, render time increases with resolution. 

With 240 rendered frames for each configuration (10s video at 24 FPS), the complete dataset will be **INSERT GB** and take **INSERT** to generate. 

In total, there will be **INSERT NUMBER** of raw image and raw depth pairs. 

An example of the folder organisation is provided below. Each render is indexed in by the configuration settings. 

INSERT SCREENSHOT 



<!-- - raw RGB and depth images  
- one render = 4 frames
- Predicted size and time of dataset
- over features
-- Table/list
-- Table with render times for water conditions/depth configurations? (21 rows -- reference and put somewhere else?)
 -->


## Testing with a Sample Dataset

change to testing with samples 

then do sample dataset
and another with render disabled to test it iterates through configurations correctly 

(Add in changing export path)
(quick test, however do still need to change the export path)
(explained in tutorial, but some renders can be changed in python but others haven't been)


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



### How to Add Components 

<!-- Describing adding into blender manually 
then configured in python scripts
- since easier to visualise and confirm changes, and GUI is intuitive and just much easier

link useful tutorials 

use things as inspiration, copy from a base and build/experiment from there  -->


## Notes for Improvement

Currently a subset of everyday ShapeNet objects have been manually selected, imported and organised into collections that are iterated over. This object import could be automated in the dataset generation script, where objects stored in the ShapeNet folder are called on each iteration. 


Further work on determining if it is possible to change the output render path for exports from the Compositing nodes. (Benefit, would ease onboaridng process etc).


## Contact: 
<otur3695@uni.sydney.edu.au>

Oliver Turner (UG student at USYD, finishing Sem 2 2026)

LinkedIn: <www.linkedin.com/in/oliver-turner-635254291>


## References

<!-- SHAPENET -->
