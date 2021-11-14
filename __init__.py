'''
#############################################
# 
# Changelog
# 


## [0.0.6.2] - 2021-13-11
### Fixed
- Error in panel

## [0.0.6.1] - 2021-01-11
### Fixed
- Environment node uses "Environment" a very often, added this to check for old enviremont textures
- Correct default Saturation values in Node Group

## [0.0.6] - 2021-31-10
### Added
- auto-transfer old environment texture images > prevents from relinking them when switching modes

## [0.0.5] - 2021-30-10
### Changed
- World Control is now created in its own world named "WorldControl"

### Added
- Clean old setup when switching between advanced and basic
- WorldControl has its own world, so we dont mess with user own setup worlds. Easier for cleaning
- Easy switching operator, switch easy between basic and advanced

## [0.0.4] - 2021-30-10
### Changed
- Moved panel to View category
- Panel header > changed dynamic header name. Font size issue, draw_header shows small font?!?

## [0.0.3] - 2021-29-10
### Added
- Reset operator > set all inputs to default
- Panel view easy access from 3d viewport

## [0.0.2] - 2021-28-10
### Fixed 
- The Add function was visible in materials nodes as well, it added empty node in material, added poll to custom nodecategrory 
 
### Changed
- Simplified node names on category, stripped "control"
- NodeGroup width was to narrow, added width

### Added
- Changelog to repo

## [0.0.1] - 2021-27-10
### Added 
- Initial release repo 

# 
#############################################
'''


import os
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from . import wc_3dv_panel
# from bpy_extras.object_utils import AddObjectHelper


bl_info = {
    "name": "World Control",
    "author": "Rombout Versluijs, Lech Sokolowski (Chocofur)",
    "version": (0, 0, 6,2),
    "blender": (2, 80, 0),
    "location": "World > Add Node > World Control",
    "description": "Adds a shader setup which allows more control when using HDR/EXR lighting. Based on Lech Sokolowski (Chocofur) video BCON19.",
    "doc_url"   : "https://github.com/schroef/World_Control/",
    "tracker_url": "https://github.com/schroef/World_Control/issues",
    "category": "World",
}


class WRD_OT_DeleteWorldControlBasic(Operator):
    """Create a new World add World Control with basic settings"""
    bl_idname = "world.delete_world_control"
    bl_label = "Delete World Control"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        PrincipledWorldWrapper
        principled_world = PrincipledWorldWrapper(world)
        world_output = principled_world.node_out
        for item in nodes:
            if item != world_output:
                # Skip over these when user adds WorldControl from different world 
                # Otherwise we end with an empty fake custom node
                if item.name != "Basic World" and item.name != "Advanced World":
                    nodes.remove(item)

        # self.report({'INFO'}, "Added Basic World Control")
        return {'FINISHED'}


# Source: LilySurfaceSrapper addon
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

# Source: Thea Render > altered
def get_env_image(context, org_world, img_type):
    '''Search for environment nodes and get image tetures

        :param context: context
        :param org_world: original worl dwhere we look for environemnt texture image
        :param img_type: look what environment image type we need; lgiht or background
        :type image: string
    '''

    # scn = context.scene
    # images = bpy.data.images
    nodes = org_world.node_tree.nodes
    env_node = [item for item in nodes if item.type =='TEX_ENVIRONMENT']

    if env_node:
        for img in env_node:
            # Light HDR
            if img_type == "Light":
                if "Environment Texture" == img.name or "Environment" == img.name:
                    old_img = img.image
            # Background HDR
            if img_type == "Background":
                if "Environment Texture.001" == img.name:
                    old_img = img.image
                    # print(img.name)
                    # print(old_img.name)
                # We are using basic so add this to background when advanced
                else:
                    old_img = img.image

        return old_img

# Source: LilySurfaceScraper
# https://github.com/eliemichel/LilySurfaceScraper/blob/b1e7066f94b965bab90696e0be75faa44eb08c3e/blender/LilySurfaceScraper/CyclesWorldData.py
def getGroundHdriNodeGroup(controlType):
    if ("WorldControl"+controlType) not in bpy.data.node_groups:
        blendfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "worldcontrol.blend")
        section = "\\NodeTree\\"
        object = "WorldControl" + controlType
        filepath = blendfile + section + object
        directory = blendfile + section
        filename = object

        bpy.ops.wm.append(
            filepath=filepath,
            filename=filename,
            directory=directory)
    return bpy.data.node_groups["WorldControl"+controlType]


def addWorldControl(self, context,controlType):
    scn = bpy.context.scene
    # Create New world
    if bpy.data.worlds.find("WorldControl") == -1:
        world = bpy.data.worlds.new("WorldControl")
    else:
        world = bpy.data.worlds["WorldControl"]    

    # org_world so we can delete fake custom node later
    org_world = bpy.context.scene.world
    scn.world = world
    world.use_nodes = True

    nodes = world.node_tree.nodes
    links = world.node_tree.links

    PrincipledWorldWrapper
    principled_world = PrincipledWorldWrapper(world)
    world_output = principled_world.node_out
    world_loc = world_output.location

    # store old environment images
    old_light_img = get_env_image(context, org_world, img_type="Light")
    old_background_img = get_env_image(context, org_world, img_type="Background")

    # Clear old node setup
    bpy.ops.world.delete_world_control()

    # Add World Control node group
    ground_hdri_node = nodes.new(type="ShaderNodeGroup")
    ground_hdri_node.name = "WorldControl"+controlType
    ground_hdri_node.label = "WorldControl"+controlType
    ground_hdri_node.node_tree = getGroundHdriNodeGroup(controlType)
    ground_hdri_node.width = 185
    ground_hdri_node.location = [world_loc.x - 235, world_loc.y]

    # Shade Node Types
    # https://docs.blender.org/api/current/bpy.types.html
    texture_light_node = nodes.new(type="ShaderNodeTexEnvironment")
    texture_light_node.location = [ground_hdri_node.location.x - 300, world_loc.y]
    texture_light_node.image = old_light_img
    if controlType == "Advanced":
        texture_bg_node = nodes.new(type="ShaderNodeTexEnvironment")
        texture_bg_node.location = [ground_hdri_node.location.x - 300, world_loc.y - 200]
        texture_bg_node.image = old_background_img
    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.location = [texture_light_node.location.x - 200, world_loc.y]
    texture_coor = nodes.new(type="ShaderNodeTexCoord")
    texture_coor.location = [mapping_node.location.x - 200, world_loc.y]

    # Setup node links
    links.new(texture_coor.outputs["Generated"], mapping_node.inputs["Vector"])
    links.new(mapping_node.outputs[0], texture_light_node.inputs[0])
    links.new(texture_light_node.outputs["Color"], ground_hdri_node.inputs["Light HDR"])
    if controlType == "Advanced":
        links.new(mapping_node.outputs[0], texture_bg_node.inputs[0])
        links.new(texture_bg_node.outputs["Color"], ground_hdri_node.inputs["Background HDR"])
    links.new(ground_hdri_node.outputs[0], world_output.inputs["Surface"])

    # Return orginal world so we clean fake custom node
    scn.world = org_world
    scn.world = world
    return org_world
    

class WRD_OT_AddWorldControlBasic(Operator):
    """Create a new World add World Control with basic settings"""
    bl_idname = "world.add_world_control_basic"
    bl_label = "Add World Control Basic"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.wc_check_mode = "Basic"
        # We use org_world to be able to delete custo node
        org_world = addWorldControl(self,context, "Basic")
        nodes = org_world.node_tree.nodes
        if nodes.find("Basic World") != -1:
            nodes.remove(nodes["Basic World"])
        self.report({'INFO'}, "Added Basic World Control")
        return {'FINISHED'}


class WRD_OT_AddWorldControlAdvanced(Operator):
    """Create a new World add World Control with advanced settings"""
    bl_idname = "world.add_world_control_advanced"
    bl_label = "Add World Control Advanced"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.wc_check_mode = "Advanced"
        # We use org_world to be able to delete custo node
        org_world = addWorldControl(self,context, "Advanced")
        nodes = org_world.node_tree.nodes
        if nodes.find("Advanced World") != -1:
            nodes.remove(nodes["Advanced World"])
        self.report({'INFO'}, "Added Advanced World Control")
        return {'FINISHED'}


class ShaderNodeBasic(bpy.types.NodeCustomGroup):
    bl_name='ShaderNodeBasic'
    bl_label='Basic World'

    def init(self, context):
        # We use org_world to be able to delete custo node
        org_world = addWorldControl(self,context, "Basic")
        nodes = org_world.node_tree.nodes
        nodes.remove(nodes["Basic World"])
        bpy.context.scene.wc_check_mode = "Basic"


class ShaderNodeAdvanced(bpy.types.NodeCustomGroup):
    bl_name='ShaderNodeAdvanced'
    bl_label='Advanced World'

    def init(self, context):
        # We use org_world to be able to delete custo node
        org_world = addWorldControl(self,context, "Advanced")
        nodes = org_world.node_tree.nodes
        nodes.remove(nodes["Advanced World"])
        bpy.context.scene.wc_check_mode = "Advanced"


from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
from nodeitems_builtins import ShaderNodeCategory
from nodeitems_utils import NodeCategory, NodeItem


class ShaderWorldNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        # From Extra Material List addon > MeshLogic
        sdata = context.space_data
        return sdata.shader_type == 'WORLD'


node_categories = [ShaderWorldNodeCategory("WRL_NEW_CUSTOM","World Control",
                                        items=[NodeItem("ShaderNodeBasic",label ='Basic'),
                                                NodeItem("ShaderNodeAdvanced",label ='Advanced')])] 

# Call control mode > allows for easy switching
# Source: https://blender.stackexchange.com/questions/70710/how-to-execute-an-operator-from-an-enumproperty
def update_control_mode(self, context):
    eval('bpy.ops.%s()' % self.wc_switch_control)


classes = [
    ShaderNodeBasic,
    ShaderNodeAdvanced,
    WRD_OT_DeleteWorldControlBasic,
    WRD_OT_AddWorldControlBasic,
    WRD_OT_AddWorldControlAdvanced
]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)
   
    register_node_categories("WCN_CUSTOM_NODES", node_categories)
    wc_3dv_panel.register()
    bpy.types.Scene.wc_check_mode = StringProperty(name="Mode",default="Basic",description="What control type are we using")#,update=wc_3dv_panel.check_world_wc_check_mode)
    bpy.types.Scene.wc_switch_control = bpy.props.EnumProperty(
            name = "Mode",
            description = "Switch contorl mode, switch between Basic and Advanced controls.",
            items = [
                ("world.add_world_control_basic", "Basic", "Basic mode allows for light, diffuse, background and glossy controls"),
                ("world.add_world_control_advanced", "Advanced", "Basic mode allows for light, diffuse, background, reflection and glossy controls. Each items also has both strength and saturation. User can set different background for lighting and background."),              
            ],
            update=update_control_mode
        )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregister_node_categories("WCN_CUSTOM_NODES")
    del bpy.types.Scene.wc_check_mode
    wc_3dv_panel.unregister()


if __name__ == "__main__":
    register()
