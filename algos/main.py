import bpy
import laspy

las_file = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las", mode="r")


# mesh arrays
verts = []  # the vertex array
faces = []  # the face array
 
# scaling factors
scaleX = 1e-7
scaleY = 1e-8
scaleZ = 1e-3

for i in range(int(len(las_file.X)/100)):
    verts.append((las_file.X[i]*scaleX, las_file.Y[i]*scaleY, las_file.Z[i]*scaleZ))

#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)