import os
import bpy
from bpy.types import Operator
# from bpy_extras.object_utils import AddObjectHelper

bl_info = {
    "name": "World Control",
    "author": "Rombout Versluijs, Lech Sokolowski (Chocofur)",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "World > Add Node > World Control",
    "description": "Adds a shader setup which allows more control when using HDR/EXR lighting. Based on Lech Sokolowski (Chocofur) video BCON19.",
    "doc_url"   : "https://github.com/schroef/World_Control/",
    "tracker_url": "https://github.com/schroef/World_Control/issues",
    "category": "World",
}


# from bpy.utils import register_class, unregister_class
blendFile = "World_Control_Worldnode.blend"


class PrincipledWorldWrapper:
    """This is a wrapper similar in use to PrincipledBSDFWrapper (located in
    bpy_extras.node_shader_utils) but for use with worlds. This is required to
    avoid relying on node names, which depend on Blender's UI language settings
    (see issue #7) """

    def __init__(self, world):
        self.node_background = None
        self.node_out = None
        for n in world.node_tree.nodes:
            if self.node_background is None and n.type == "BACKGROUND":
                self.node_background = n
            elif self.node_out is None and n.type == "OUTPUT_WORLD":
                self.node_out = n

# Source LilySurfaceScraper
# https://github.com/eliemichel/LilySurfaceScraper/blob/b1e7066f94b965bab90696e0be75faa44eb08c3e/blender/LilySurfaceScraper/CyclesWorldData.py
def getGroundHdriNodeGroup(controlType):
    if ("WorldControl"+controlType) not in bpy.data.node_groups:
        blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "worldcontrol.blend")
        section = "\\NodeTree\\"
        object = "WorldControl" + controlType
        filepath = blendfile + section + object
        directory = blendfile + section
        filename = object
#        print(filepath)
#        print(directory)
#        print(filename)
        bpy.ops.wm.append(
            filepath=filepath,
            filename=filename,
            directory=directory)
    return bpy.data.node_groups["WorldControl"+controlType]


def addWorldControl(self, context,controlType):
    #    world = bpy.data.worlds.new(name=self.name)
    # Create New world
    # if bpy.data.worlds.find("World-Control") == -1:
    #     world = bpy.data.worlds.new("World-Control")
    # else:
    #     world = bpy.data.worlds["World-Control"]
    world = bpy.context.scene.world
    world.use_nodes = True

    nodes = world.node_tree.nodes
    links = world.node_tree.links
    PrincipledWorldWrapper
    principled_world = PrincipledWorldWrapper(world)
    world_output = principled_world.node_out
    world_loc = world_output.location

    ground_hdri_node = nodes.new(type="ShaderNodeGroup")
    ground_hdri_node.node_tree = getGroundHdriNodeGroup(controlType)
    ground_hdri_node.location = [world_loc.x - 200, world_loc.y]
    # Shade Node Types
    # https://docs.blender.org/api/current/bpy.types.html
    texture_light_node = nodes.new(type="ShaderNodeTexEnvironment")
    texture_light_node.location = [ground_hdri_node.location.x - 300, world_loc.y]
    if controlType == "Advanced":
        texture_bg_node = nodes.new(type="ShaderNodeTexEnvironment")
        texture_bg_node.location = [ground_hdri_node.location.x - 300, world_loc.y - 200]
    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.location = [texture_light_node.location.x - 200, world_loc.y]
    texture_coor = nodes.new(type="ShaderNodeTexCoord")
    texture_coor.location = [mapping_node.location.x - 200, world_loc.y]

    links.new(texture_coor.outputs["Generated"], mapping_node.inputs["Vector"])
    links.new(mapping_node.outputs[0], texture_light_node.inputs[0])
    links.new(texture_light_node.outputs["Color"], ground_hdri_node.inputs["Light HDR"])
    if controlType == "Advanced":
        links.new(mapping_node.outputs[0], texture_bg_node.inputs[0])
        links.new(texture_bg_node.outputs["Color"], ground_hdri_node.inputs["Background HDR"])
    links.new(ground_hdri_node.outputs[0], world_output.inputs["Surface"])


class WRD_OT_AddWorldControlBasic(Operator):
    """Create a new World add World Control with basic settings"""
    bl_idname = "world.add_world_control_basic"
    bl_label = "Add World Control Basic"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addWorldControl(self,context, "Basic")
        self.report({'INFO'}, "Added Basic World Control")
        return {'FINISHED'}


class WRD_OT_AddWorldControlAdvanced(Operator):
    """Create a new World add World Control with advanced settings"""
    bl_idname = "world.add_world_control_advanced"
    bl_label = "Add World Control Advanced"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        addWorldControl(self,context, "Advanced")
        self.report({'INFO'}, "Added Advanced World Control")
        return {'FINISHED'}


class ShaderNodeBasic(bpy.types.NodeCustomGroup):
    bl_name='ShaderNodeBasic'
    bl_label='Basic World'

    def init(self, context):
        addWorldControl(self,context, "Basic")
        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        nodes.remove(nodes["Basic World"])


class ShaderNodeAdvanced(bpy.types.NodeCustomGroup):
    bl_name='ShaderNodeAdvanced'
    bl_label='Advanced World'

    def init(self, context):
        addWorldControl(self,context, "Advanced")
        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        nodes.remove(nodes["Advanced World"])


from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
from nodeitems_builtins import ShaderNodeCategory

node_categories = [ShaderNodeCategory("WRL_NEW_CUSTOM","World Control",
                                        items=[NodeItem("ShaderNodeBasic",label ='Basic Controls'),
                                                NodeItem("ShaderNodeAdvanced",label ='Advanced Controls')])] 


classes = [
    ShaderNodeBasic,
    ShaderNodeAdvanced,
    WRD_OT_AddWorldControlBasic,
    WRD_OT_AddWorldControlAdvanced
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_node_categories("WCN_CUSTOM_NODES", node_categories)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregister_node_categories("WCN_CUSTOM_NODES")


if __name__ == "__main__":
    register()
