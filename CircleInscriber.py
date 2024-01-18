import bpy
import math

point1 = (0,0,0)
point2 = (0,0,0)
BigR = 0.4
distance = 1.2

def Button1(context):
    mode = bpy.context.active_object.mode
    
    # we need to switch from Edit mode to Object mode so the selection gets updated
    bpy.ops.object.mode_set(mode='OBJECT')
    distance = context.scene.Distance_to_center
     #gets location of centers of both sorrounding circles
    for o in bpy.context.selected_objects:
        selectedVerts = [v for v in o.data.vertices if v.select]
        BigR = o.dimensions.x/2
        loc = o.location

        bpy.ops.object.mode_set(mode=mode)
        if o == bpy.context.selected_objects[0]:
            point1 = loc
        if o == bpy.context.selected_objects[1]:
            point2 = loc

    p1 = point1
    p2 = point2
    
    mid = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2,0)
    newcenter = create_point_on_line(Point(0,0,0),mid,distance)
    
    # d is dist from the new center to center of either of the sorrounding circles since they are both equidistant
    d = math.sqrt((newcenter.x - p1.x)**2 + (newcenter.y - p1.y)**2)
    #radius of our new circle will just be that distance - raduis of either sorrounding circles
    rad = d-BigR

    bpy.ops.mesh.primitive_circle_add(radius = rad, enter_editmode=False, align='WORLD', location= (newcenter.x,newcenter.y,0), scale=(1, 1, 1))
    vpoint = create_point_on_line(Point(0,0,0),mid,distance)
    

#given two points, this method calculates the line they are on and then uses "distance" to determine how far from the origin the new center will be
def create_point_on_line(point1, point2, distance):
    # Calculate the total distance between point1 and point2
    total_distance = ((point2.x - point1.x)**2 + (point2.y - point1.y)**2)**0.5

    # Calculate the ratio to determine the position of the new point
    ratio = distance / total_distance

    # Calculate the coordinates of the new point
    new_point_x = point1.x + ratio * (point2.x - point1.x)
    new_point_y = point1.y + ratio * (point2.y - point1.y)

    return Point(new_point_x, new_point_y, 0)    

class Point:
    def __init__(self, x, y,z):
        self.x = x
        self.y = y
        self.z = z
    

class drawCircle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.draw"
    bl_label = "draw Circle"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Button1(context)
        return {'FINISHED'}
    

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Add tangent circle"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

       

        # Big render button
        layout.label(text="Select the two encompassing circles:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.draw")
        
        
        
        layout.prop(context.scene, "Distance_to_center", text="Distance to center")
        

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).


def register():
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(drawCircle)
    bpy.types.VIEW3D_MT_object.append(menu_func)
     # Add the properties to the scene
    bpy.types.Scene.Distance_to_center = bpy.props.FloatProperty(
        name="Distance to center",
        description="Enter a floating-point number",
        default=0.0,
        min=0.0,
        max=10.0
    )


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    del bpy.types.Scene.Distance_to_center

if __name__ == "__main__":
    register()
