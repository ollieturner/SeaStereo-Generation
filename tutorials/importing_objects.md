# TUTORIAL

## Importing Objects into Blender

### Aim
This tutorial explains how to import objects into Blender and provides sources for finding such objects. 


### Background
To create an underwater scene with a realistic seafloor environment and objects of interest for imaging, objects should be imported from third-party sources. This is faster and produces better quality than making things yourself.


### Initial Configuration

The scene is organised into the following collections:

| Collection         | Description                                                             |
|--------------------|-------------------------------------------------------------------------|
| Sand Seafloors     | Colour and texture for sand seafloor plane                              |
| Background Objects | Seafloor objects in background e.g. rocks, seaweed, shipwreck |
| Everyday Objects   | Objects of interest in foreground and randomly positioned               |

This setup is followed in the .blend file and in the blender_files/ folder. 


### Third-Party Sites


<!-- REPLACE WITH TABLE


#### Sand Seafloor

The sand seafloor material was sourced from: https://ambientcg.com/view?id=Ground054. This is a very good resource for many other materials and environments.  

#### Background Objects



For background objects

two ebsites, put in example objects

#### Everyday Objects

Can find on websites, but for easy access, large dataset, used for current tabletop datasets so interested in submerging the objects
ShapeNet
Say how need to make account and go through 2 layers of approval and need a Hugging face account, so will take a 2-3 days before can start using 

shapenet: https://shapenet.org/
shapenet categories: https://shapenet.org/taxonomy-viewer 
number -- category translator: https://shapenet.org/resources/data/shapenetcore.taxonomy.json  -->




### Instructions

First download the desired object from the sources provided above or from your own research. Make sure the object comes with files to describe its material e.g. normals, colour. The ShapeNet everyday objects are .obj files and come with the material properties files. 

After downloading, the object can be imported from the File menu, as shown below. Then navigate to the .obj's location and enter.

INSERT PHOTO

Position and scale (to re-size) the object as needed. 

To move it into a collection in the control panel on the right, select the object and press 'M'.

Also, sometimes the faces of the ShapeNet objects are jagged and zebram pattern-like. Right click the object and 'Auto-Smooth' it. 





