import bpy, mathutils
from math import sqrt

bl_info = {
    'name': 'Curve Merge Segments by distance',
    'author': 'Craig Smith',
    'version': (1, 0),
    'blender': (3, 6, 2),
    'location': 'View3D > Context menu (W/RMB) > Merge Segments by Distance',
    'description': 'Merges segments with overlapping ends',
    'category': 'Object'
}

# This needs to be a seperate function because spline array changes
def merge_spline(context, tolerance):
    obj = context.active_object
    mergelist = []
    
    curve_data = obj.data
    
    num_splines = len(curve_data.splines)
    num_points = len(curve_data.splines[0].points)
    bpy.ops.curve.select_all(action='DESELECT')

    # Iterate through all splines
    for spline_i in range(num_splines):
        num_points_i = len(curve_data.splines[spline_i].points)
        for spline_j in range(spline_i+1, num_splines):
            
            # Iterate through each point on each spline
            num_points_j = len(curve_data.splines[spline_j].points)           
            for point_i in range(0, num_points_i):
                segment1 = curve_data.splines[spline_i].points[point_i:point_i + 2]
                for point_j in range(0, num_points_j):
                    segment2 = curve_data.splines[spline_j].points[point_j:point_j + 2]
                    
                    # Check both coords on the segment
                    for coord_i in range(len(segment1)):
                        coord1 = segment1[coord_i].co
                        for coord_j in range(len(segment2)):
                            coord2 = segment2[coord_j].co
                    
                            distance = sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))
                    
                            if distance <= tolerance:
                                print(f"Selecting {spline_i} {segment1[coord_i].co} and  {spline_j} {segment2[coord_j].co}")
                                segment1[coord_i].select = True # index 1?
                                segment2[coord_j].select = True
                                
                                # Update the scene to reflect the selection
                                bpy.context.view_layer.update()
                                
                                try:
                                    bpy.ops.curve.make_segment()
                                    num_splines = num_splines - 1
                                    return True  # We only do one at a time!
                                except Exception as e:
                                    print(e)
                                
                                # Clear the selection after creating the segment
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.mode_set(mode='EDIT')
                                
                                bpy.ops.curve.select_all(action='DESELECT')
    return False  # No changes were made

def main(context, tolerance = 0.0):
    
    count = 0
    
    for splines in range(len(context.active_object.data.splines)):
        if merge_spline(context, tolerance):
            count = count + 1
        else:
            return count
    
    return count
    


class CurveRemvDbs(bpy.types.Operator):
    """Merge consecutive segments that are near to each other"""
    bl_idname = 'curve.remove_dup_segments'
    bl_label = 'Remove Segments by Distance'
    bl_options = {'REGISTER', 'UNDO'}

    distance: bpy.props.FloatProperty(name = 'Distance', default = 0.0, min = 0.0, max = 10.0, step = 1)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'CURVE')

    def execute(self, context):
        removed=main(context, self.distance)
        self.report({'INFO'}, "Merged %d overlaping segments" % removed)
        return {'FINISHED'}




def menu_func(self, context):
    self.layout.operator(CurveRemvDbs.bl_idname, text='Merge Segments by Distance')

def register():
    bpy.utils.register_class(CurveRemvDbs)
    bpy.types.VIEW3D_MT_edit_curve_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CurveRemvDbs)
    bpy.types.VIEW3D_MT_edit_curve_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()


