
import bpy, os, re
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty
from bpy.types import Panel, Operator, Menu


def engine_compatibility(context):
    scn = context.scene
    return scn.render.engine == 'CYCLES'

def find_basic(nt):
    return nt.nodes.find("WorldControlBasic")

def find_advanced(nt):
    return nt.nodes.find("WorldControlAdvanced")
    
def check_world_wc_check_mode(self, context):
    # Dirty method to get around 'RestrictContext'
    sceneLoaded = False
    try:
        if bpy.context.scene:
            sceneLoaded = True
    except:
        pass

    if sceneLoaded:
        scn = context.scene
        world = scn.world
        nt = world.node_tree
        if find_basic(nt) != -1:
            scn.wc_check_mode = "Basic"
        if find_advanced(nt) != -1:
            scn.wc_check_mode = "Advanced"
        else:
            scn.wc_check_mode = "World Control"

def check_world_control_type(context):
    world = bpy.context.scene.world
    nt = world.node_tree
    if find_basic(nt) != -1:
        return "World Control Basic"
    if find_advanced(nt) != -1:
        return "World Control Advanced"
    else:
        return "World Control"


def return_world_control_type():
    world = bpy.context.scene.world
    nt = world.node_tree
#    print(find_basic(nt) != -1)
    if find_basic(nt) != -1:
        return "WorldControlBasic"
    if find_advanced(nt) != -1:
        return "WorldControlAdvanced"
    else:
        return "World Control"


class WorldControlPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'View'
    bl_options = {'DEFAULT_CLOSED'}


class WC_PT_main_panel(WorldControlPanel, Panel):          
    bl_label = "World Control"
    #bl_context = "objectmode"

    # wc_check_mode : StringProperty(name="ControlType",default = "Basic")

#     @classmethod
#     def poll(cls, context):
#         world = bpy.context.scene.world
#         nt = world.node_tree
#         basic = find_basic(nt)
#         advanced = find_advanced(nt)
# #        print(engine_compatibility(context))
# #        print(basic or advanced != -1)
#         return (basic != -1 or advanced != -1) and engine_compatibility(context)
    
    # Header text looks different vs regular BL_name > check with devs
    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text=str(check_world_control_type(context)))

        
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        scn = context.scene
        world = scn.world
        nodes = scn.world.node_tree.nodes
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)

        col = layout.column(align=False, heading="Mode")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)

        if engine_compatibility and (basic != -1 or advanced != -1):
            sub.prop(scn,"wc_switch_control",expand = True)
            # sub.prop(scn, "wc_check_mode", emboss=False,icon='WORLD')
            # sub.label(text=str(check_world_wc_check_mode(context))) #icon='WORLD_DATA'
            reset_bg = row.operator("wc.reset_settings", icon = 'LOOP_BACK', text='')
            reset_bg.controlType = return_world_control_type()

            col = layout.column()
            col.separator()
            col.prop(nodes['Mapping'].inputs[2], "default_value", text = 'Rotation')   
        
        col = layout.column()
        if (basic == -1 and advanced == -1):   
            col.label(text = 'No World Control in shader', icon = 'INFO') 
        if not engine_compatibility:
            col.label(text = 'Not compatible with this render engine', icon = 'INFO')
            col.prop(scn.render, 'engine')
        # else:


class WC_PT_light_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Light"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
#        print(basic or advanced != -1)
        return (basic != -1 or advanced != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene
                 
        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        controlType = return_world_control_type()  
        
#        col.prop(nodes['Mapping'].inputs[2], "default_value", text = 'Rotation')   
             
        if controlType == 'WorldControlBasic':
            col.prop(nodes['WorldControlBasic'].inputs[1], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlBasic'].inputs[2], "default_value", text = 'Temperature')
            
            
        if controlType == 'WorldControlAdvanced':
            col.prop(nodes['WorldControlAdvanced'].inputs[1], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlAdvanced'].inputs[2], "default_value", text = 'Saturation')
            col.prop(nodes['WorldControlAdvanced'].inputs[3], "default_value", text = 'Temperature')


class WC_PT_background_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Background"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
        return (basic != -1 or advanced != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene

        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        
        controlType = return_world_control_type()  
     
        if controlType == 'WorldControlBasic':
            col.prop(nodes['WorldControlBasic'].inputs[3], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlBasic'].inputs[4], "default_value", text = 'Saturation')
            
        if controlType == 'WorldControlAdvanced':
            col.prop(nodes['WorldControlAdvanced'].inputs[7], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlAdvanced'].inputs[8], "default_value", text = 'Saturation') 


class WC_PT_diffuse_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Diffuse"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
        return (basic != -1 or advanced != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene

        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        
        controlType = return_world_control_type()  
     
        if controlType == 'WorldControlBasic':
            col.prop(nodes['WorldControlBasic'].inputs[5], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlBasic'].inputs[6], "default_value", text = 'Saturation')      
            
        if controlType == 'WorldControlAdvanced':
            col.prop(nodes['WorldControlAdvanced'].inputs[4], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlAdvanced'].inputs[5], "default_value", text = 'Saturation')                         


class WC_PT_reflections_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Reflections"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
        return (advanced != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene

        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        
        controlType = return_world_control_type()  
     
        if controlType == 'WorldControlAdvanced':
            col.prop(nodes['WorldControlAdvanced'].inputs[9], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlAdvanced'].inputs[10], "default_value", text = 'Saturation') 


class WC_PT_glossy_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Glossy"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
        return (basic != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene

        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        
        controlType = return_world_control_type()  
     
        if controlType == 'WorldControlBasic':
            col.prop(nodes['WorldControlBasic'].inputs[7], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlBasic'].inputs[8], "default_value", text = 'Saturation')   


class WC_PT_refraction_settings(WorldControlPanel, Panel):
    bl_category = "View"
    # bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Refraction"
    bl_parent_id = "WC_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        world = bpy.context.scene.world
        nt = world.node_tree
        basic = find_basic(nt)
        advanced = find_advanced(nt)
        return (advanced != -1) and engine_compatibility(context)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False
        scn = context.scene

        col = layout.column(align=True)                
        nodes = scn.world.node_tree.nodes
        
        controlType = return_world_control_type()  
        
        if controlType == 'WorldControlAdvanced':
            col.prop(nodes['WorldControlAdvanced'].inputs[11], "default_value", text = 'Strength')
            col.prop(nodes['WorldControlAdvanced'].inputs[12], "default_value", text = 'Saturation')            



def reset_settings(controlType):
    scn = bpy.context.scene
    worlds = bpy.data.worlds
    world = scn.world
    nodes = world.node_tree.nodes
    
    # Light
    if controlType == 'WorldControlBasic':
        nodes['WorldControlBasic'].inputs[1].default_value = 1.0 # Strength
        nodes['WorldControlBasic'].inputs[2].default_value = 5500 # Temperature

    if controlType == 'WorldControlAdvanced':
        nodes['WorldControlAdvanced'].inputs[1].default_value = 1.0 # Strength
        nodes['WorldControlAdvanced'].inputs[2].default_value = 0.5 # Saturation
        nodes['WorldControlAdvanced'].inputs[3].default_value = 5500 # Temperature

    # Background
    if controlType == 'WorldControlBasic':
        nodes['WorldControlBasic'].inputs[3].default_value = 1.0 # Strength
        nodes['WorldControlBasic'].inputs[4].default_value = 0.5 # Saturation
        
    if controlType == 'WorldControlAdvanced':
        nodes['WorldControlAdvanced'].inputs[7].default_value = 1.0 # Strength
        nodes['WorldControlAdvanced'].inputs[8].default_value = 0.5 # Saturation

    # Diffuse
    if controlType == 'WorldControlBasic':
        nodes['WorldControlBasic'].inputs[5].default_value = 1.0 # Strength
        nodes['WorldControlBasic'].inputs[6].default_value = 0.5 # Saturation
        
    if controlType == 'WorldControlAdvanced':
        nodes['WorldControlAdvanced'].inputs[4].default_value = 1.0 # Strength
        nodes['WorldControlAdvanced'].inputs[5].default_value = 0.5 # Saturation

    # Reflections
    if controlType == 'WorldControlAdvanced':
        nodes['WorldControlAdvanced'].inputs[9].default_value = 1.0 # Strength
        nodes['WorldControlAdvanced'].inputs[10].default_value = 0.5 # Saturation
    # Glossy
    if controlType == 'WorldControlBasic':
        nodes['WorldControlBasic'].inputs[7].default_value = 1.0 # Strength
        nodes['WorldControlBasic'].inputs[8].default_value = 0.5 # Saturation

    # Refraction
    if controlType == 'WorldControlAdvanced':
        nodes['WorldControlAdvanced'].inputs[11].default_value = 1.0 # Strength
        nodes['WorldControlAdvanced'].inputs[12].default_value = 0.5 # Saturation


class WC_OT_reset_settings(Operator):
    bl_idname = "wc.reset_settings"
    bl_label = "Reset"
    bl_description = "Reset to Default Values"
    bl_options = {'REGISTER', 'UNDO'}
    
    controlType : StringProperty(default = 'WorldControlBasic')
    
    # @classmethod
    # def poll(cls, context):
    #     return check_world_nodes() == 'OK'
    
    def execute(self, context):
        controlType = return_world_control_type()
        reset_settings(controlType)
        return {'FINISHED'}

classes = (
    WC_PT_main_panel,
    WC_PT_light_settings,
    WC_PT_background_settings,
    WC_PT_diffuse_settings,
    WC_PT_reflections_settings,
    WC_PT_glossy_settings,
    WC_PT_refraction_settings,
    WC_OT_reset_settings
    )
    

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)       

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)        



if __name__ == "__main__":
    register()        