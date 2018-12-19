import bpy
import laspy

las_file = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000015/AK_BrooksCamp_2012_000015.las", mode="r")

# mesh arrays
verts = []  # the vertex array
faces = []  # the face array
 
# scaling factors
scaleX, scaleY, scaleZ = las_file.header.scale
offsetX, offsetY, offsetZ = las_file.header.offset

for i in range(len(las_file.X)):
    verts.append((las_file.X[i]*scaleX + offsetX, las_file.Y[i]*scaleY + offsetY, las_file.Z[i]*scaleZ + offsetZ))

#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
