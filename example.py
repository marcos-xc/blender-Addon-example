import bpy
from bpy.props import(
    IntProperty,
    FloatProperty,
    BoolProperty,
    StringProperty,
    PointerProperty,
    EnumProperty,
)

class ExamplePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_example_tools"
    bl_label = "Example Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Tools"

    def draw(self, context):
        props = context.scene.example_props
        layout = self.layout
        col = layout.column()
        col.label(text = "示例1")
        col.prop(props,"cube_size", text = "Cube Size")
        col.operator("example.create_cube", text = "Create Cube")
        
        col.label(text = "示例2")
        col.prop(props, "objs_count", text = "物体数量")
        col.operator("example.get_obj_info", text = "获取当前物体数量")
        
        col.label(text = "示例3")
        col.operator("example.set_unit", text = "设置单位")
        
        col.label(text = "示例4")
        col.prop(props, "obj_list", text = "物体列表")
        col.prop(props, "current_name", text = "当前命名")
        col.prop(props, "case_option", text = "大小写")
        
        
        
        
class CreateCubeOperator(bpy.types.Operator):
    bl_idname = "example.create_cube"
    bl_label = "Create Cube"

    def execute(self, context):
        props = context.scene.example_props
        bpy.ops.mesh.primitive_cube_add(size=props.cube_size, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        obj = context.object
        obj.name = "Example_Cube"
        return {'FINISHED'}
    
class SetUnitOperator(bpy.types.Operator):
    bl_idname = "example.set_unit"
    bl_label = "Set Unit Length"

    def execute(self,context):
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.length_unit = 'METERS'
        return {'FINISHED'}
    
class GetObjInfoOperator(bpy.types.Operator):
    bl_idname = "example.get_obj_info"
    bl_label = "find all objects"

    def execute(self,context):
        objs = bpy.data.objects
        props = context.scene.example_props
        props.objs_count = len(objs)
        return {'FINISHED'}

def obj_list_callback(self, context):
    objs = bpy.data.objects   
    items = []
    
    for obj in objs:
        item = (obj.name, obj.name, "")
        items.append(item)
    
    if len(objs) == 0:
        items.append(('!','!',''))
        
    return items

def update_name(self, context):
    props = context.scene.example_props
    name = props.obj_list
    if props.case_option:
        props.current_name = name.upper()
    else:
        props.current_name = name.lower()
    
class ExampleProps(bpy.types.PropertyGroup):
    cube_size: IntProperty(default = 1)
    case_option: BoolProperty(default = False, update = update_name)
    current_name: StringProperty()
    obj_list : EnumProperty(
        items= obj_list_callback,
        update = update_name,
    )
    objs_count: IntProperty()


blender_classes = [
    CreateCubeOperator,
    SetUnitOperator,
    GetObjInfoOperator,
    ExampleProps,
    ExamplePanel,
]

def register():
    for bclass in blender_classes:
        bpy.utils.register_class(bclass)
    bpy.types.Scene.example_props = PointerProperty(type=ExampleProps)
        
def unregister():
    del bpy.types.Scene.example_props
    for bclass in blender_classes:
        bpy.utils.unregister_class(bclass)
        
if __name__ == "__main__":
    register()
    

    