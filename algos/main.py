import laspy
from algos import *

sparsifyLASFile("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las",\
    "/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las",25,25,25)

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las", mode="r")
print(len(inFile.X))

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las", mode="r")
print(len(inFile.X))


'''
inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las", mode="r")
for dim in inFile.point_format:
    print(dim.name)
'''

'''

import bpy
import laspy

def getVerts(path):
    las_file = laspy.file.File(path, mode="r")

    #vertices array
    verts = []

    # scaling factors
    scaleX, scaleY, scaleZ = las_file.header.scale
    offsetX, offsetY, offsetZ = las_file.header.offset

    for i in range(len(las_file.X)):
        verts.append((las_file.X[i]*scaleX + offsetX, las_file.Y[i]*scaleY + offsetY, las_file.Z[i]*scaleZ + offsetZ))

    return verts

def plotLAS(path, name):

    #get vertices
    verts = getVerts(path)

    #create mesh and object
    mesh = bpy.data.meshes.new(name)
    object = bpy.data.objects.new(name,mesh)
    
    #set mesh location
    object.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(object)
    
    #create mesh from python data
    mesh.from_pydata(verts,[],[])

def plotLASCube(path, size):
    scene = bpy.context.scene

    verts = getVerts(path)

    cubes = []

    for vert in verts:
        bpy.ops.mesh.primitive_cube_add(location=vert)
        bpy.context.scene.objects.active.scale = (size,size,size)
        cubes.append(bpy.context.scene.objects.active)
        
    ctx = bpy.context.copy()

    # one of the objects to join
    ctx['active_object'] = cubes[0]

    ctx['selected_objects'] = cubes

    # we need the scene bases as well for joining
    ctx['selected_editable_bases'] = [scene.object_bases[cube.name] for cube in cubes]

    bpy.ops.object.join(ctx)


plotLASCube("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las", 5)    
     
'''