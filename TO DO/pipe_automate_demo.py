# Typed out from Youtube tutorial example
# (Couldn't access their files, has some issues from manual typing) 
# Use as inspiration for iterating over conditions and using classes 


# Can't render all images --> make it crash, can only do one at a time
# Have to set up a timer/interval 
# Look if still rendering. If rendering finished, then move onto the next one

# Directories: name file with configuration

import os
from os.path import exists
import bpy 

# Class
class RenderVariations(bpy.types.Operator):
    bl_idname = "render.variations"
    bl_label = "Render All Variations"
    
    # Initialise Boolean flags/variables    
    cancel_render = None
    rendering = None
    render_queue = None
    timer_event = None
    total = 0
    
    # Should delete this, not relevant
    LOGOS_PATH = "//logos"
    OUTPUT_PATH = "//output"
    
    def render_init(self, scene, depsgraph):
        self.rendering = True
        print("RENDER INIT", self.make_filename(self.render_queue[0]))
        
    def render_complete(self, scene, depsgraph):
        self.render_queue.pop(0)
        self.rendering = False
        
    def render_cancel(self, scene, depsgraph):
        self.cancel_render = True 
        print("RENDER_CANCEL")
    
    # Check if file exists    
    def exists(self, render_filename):
        output_path = self.OUTPUT_PATH + os.sep + render_filename + ".png"
        return exists(output_path) # what how is this nested 
    
    # Definition to make a filename - combination of strings to build name (will be different for mine)
    def make_filename(self, qitem):
        # 7:30
        
    # Actual starting point
    def execute (self, context):
        self.cancel_render = False
        self.rendering - False
        self.render_queue = []
        
        # Arrays of different combos (8:18)
        # Uses none as a check if it needs to be disabled 
        # Includes changing colours, objects
        
        TOPS = ["none", "Top1", "Top2", "Top3"]
        LEFTS = ["none", "Left1", "Left2", "Left3"]
        FAUCETS = ["none", "Faucet"]
        GAUGES = ["none", "Gauge"]
        FAUCET_COLORS = [
            {"color": (1, 0, 0, 1), "label": "red"}, 
            {"color": (0.985, 0.621, 0, 1), "label": "yellow"},
            {"color": (0.05, 0.05, 0.05, 1), "label": "black"}
        }
                
        cam_collections = bpy.data.collections['Cameras'] # Requires a camera collections - Front, Rear
        CAMERAS = [{"name": str(i), "value": o.name}
                    for i, o in enumerate(cam_collection.objects)]  # Should I store camera paths as different cameras or automate in here
                    
        
        ## -- Build render queue -- ##
        
        # For each logo, build something/do something
        # 10:50
        
        # loop through every possibility for rendering e.g. for cam in CAMERAS
        
        # Put through every configuration into render queue
        
        logodir - bpy.path.abspath(self.LOGOS_PATH)
        for file_path in os.listdir( logodir ):
            if (file_path.lower().endswith('.jpg') or file_path.lower().endswith('.pmg' or file_path.lower().endswith('.png')):
                logo = {"name": os.path.splitext(file_path)[0], "path": logodir + os.sep + file_path}
                
                # Then loop through every possibility 
                for cam in CAMERAS:
                    for top in TOPS:
                        for left in LEFTS:
                            for gauge in GAUGES:
                                for faucet in FAUCETS:
                                    if (faucet == "none"):
                                        self.render_queue.append({
                                            "logo": logo, 
                                            "camera": cam["value"],
                                            "top": top,
                                            "left": left, 
                                            "gauge": gauge, 
                                            "faucet": faucet, 
                                            "faucet_color": None,
                                        })
                                    else:
                                        for faucet_colour in FAUCET_COLORS:
                                            self.render_queue.append({
                                            "logo": logo, 
                                            "camera": cam["value"],
                                            "top": top,
                                            "left": left, 
                                            "gauge": gauge, 
                                            "faucet": faucet, 
                                            "faucet_color": faucet_color,
                                        })
                                        
        # Print out total number of configurations/images to render                                
        self.total = len(self.render_queue)
        print("Total: " + str(self.total))
        
        ## ---------------------- ##      
        
        # Setup handlers
        
        # Append definition to handler events 
        
        # Register callback functions
        bpy.app.handlers.render_init.clear()
        bpy.app.handlers.render_init.append(self.render_init)
        
        bpy.app.handlers.render_complete.clear()
        bpy.app.handlers.render_complete.append(self.render_complete)
        
        bpy.app.handlers.render_cancel.clear()
        bpy.app.handlers.render_cancel.append(self.render_cancel)
        
        # Lock interface (to prevent crashes)
        bpy.types.RenderSettings.use_lock_interface = True
        
        # Create timer event that runs every second to check if render_queue needs
        self.timer_event = context.window_manager.event_timer_add(0.5, window = context_window)
        
        # Register as running in the background
        context.window_manager.modal_handler_add(self)
        
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        # ESC - to cancel
        if event.type == 'ESC':
            bpy.types.RenderSettings.use_lock_interface = False
            print("CANCELLED")
            return {"CANCELLED"}
        
        # Timer event every second
        elif event.type == 'TIMER':
            # If cancelled or no items in queue to render, finish
            if (len(self.render_queue) == 0) or self.cancel_render is True:
                
                # Remove all render callbacks
                bpy.app.handlers.render_init.clear()
                bpy.app.handlers.render_complete.clear()
                bpy.app.handlers.render_cancel.clear()
                
                # Removd timer
                context.window_manager.event_timer_remove(self.timer_event)
                
                bpy.types.RenderSettings.use_lock_interface = False
                
                print("FINISHED")
                return {"FINISHED"}
            # Nothing is rendering an there are items in queue
            elif self.rendering is False:
                
                sc = bpy.context.scene
                qitem = self.render_queue[0]
                output_path = self.OUTPUT_PATH + os.step + render_filename
                
                # Skip is file exists already
                if existws(bpy.path.abspath(ooutput_path) + ".png"):
                    self.render_queue.pop(0)
                    print("Skipping " + render_filename + ", queue length: " + str(len(self.render_queue)))
                else: # we render
                    print("Rendering " + str(self.total + 1 - len(self.render_queue)
                                            ) + "/" + str(self.total) + ": " + render_filename)
                     # will do later
                     
                     # Settings for rendering
                     # This will run lots of times
                     # Set the flags (hide/render flags) on and off (to set/choose objects)
                     # Want defaults at first 
                     
                     # defaults
                     for obj in bpy.data.collections['Base'].objects:
                         obj.hide_render = False
                     for obj in bpy.data.collections['Tops'].objects:
                         obj.hide_render = False
                     for obj in bpy.data.collections['Lefts'].objects:
                         obj.hide_render = False
                         
                     # loop through all objects and hide if it is not the name we are given eg Top1, hide others except Top1     
                     # Top
                     for obj in bpy.data.collections['Tops'].objects:
                         obj.hide_render = obj.name != qitem["top"]
                     # Left
                     for obj in bpy.data.collections['Lefts'].objects:
                         obj.hide_render = obj.name != qitem["left"]
                     # Faucet (not in a collection)
                     bpy.data.collection['Base'].objects["Faucet"].hide_render = qitem["faucet"] != "Faucet"
                     
                     # Faucet color
                     # If there is a faucet (not none) then set faucet colour and material 
                     if (qitem["faucet"] != "none"):
                         print("Trying to set faucet color to " + qitem["faucet_color"]["label"])
                         mat = bpy.data.materials["Faucet"]
                         principled = mat.node_tree.nodes["Principled BSDF"]
                         principled.inputs["Base Color"].default_value = qitem["faucet_color"]["color"]
                         
                    # Gauge
                    bpy.data.collections['Base'].objects["Gauge"].hide_render = qitem["gauge"] != "Gauge"
                    
                    # Logo - link back to node diagram
                    mat = bpy.data.materials["Logo"]
                    principled = mat.node_tree.nodes["Principled BSDF"]
                    texture = principled.inputs["Base Colors".links[0].from_node
                    if (texture): #if succeeded, set property 
                        texture.image = bpy.data.images.lad(qitem["logo"]["path"])
                        
                    
                    # Change scene active camera
                    cameraName = qitem["camera"] 
                    if cameraName in sc.objects:
                        sc.camera = bpy.data.objects[cameraName]
                    else:
                        self.report(
                            {'ERROR_INVALID_INPUT'}, message = "Can no find camera "+cameraName+ "in scene!")
                        return {'CANCELLED'}
                    
                    # changeoutput path
                    sc.render.filepath = output_path
                    
                    # Command to render
                    bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
                        
                     
        return {"PASS_THROUGH"}
    
    
    
    # Need to register class then run 
    
def register():
    bpy.utils.register_class(RenderVariations)
    
def unregister():
    bpy.utils.unregister_class(RenderVariations)
    
if __name__ == "__main__":
    register()
    bpy.ops.render.variations() # name of class
    
    

    
# To render
# Run concole messages by running Blender from terminal 

# Doesn't do it in background
# Also change output path 
# where does this file even save
           
                                        
               