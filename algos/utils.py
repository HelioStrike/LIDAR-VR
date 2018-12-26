import laspy
import numpy as np

#loads raster data (.asc format)
def loadData(path):
    data = open(path).read()
    info = {field.split(' ')[0]:int(field.split(' ')[-1]) for field in data.split('\n')[:6]}

    data = data.split('\n')[7:]
    ndata = []

    for d in data:
        for x in d.split(' '):
            if x != '':
                ndata += [x]
            else:
                ndata += [info['NODATA_value']]

    ndata = [int(float(d)) for d in ndata]
    lidarmap = [ndata[i*info["ncols"]:(i+1)*info["ncols"]] for i in range(int(len(ndata)/info["ncols"]))]

    return info, lidarmap

#returns vertices from .las file (point cloud data)
def getVerts(path):
    #load the .las  file
    las_file = laspy.file.File(path, mode="r")

    #vertices array
    verts = []

    # scaling factors
    scaleX, scaleY, scaleZ = las_file.header.scale
    offsetX, offsetY, offsetZ = las_file.header.offset

    for i in range(len(las_file.X)):
        verts.append((las_file.X[i]*scaleX + offsetX, las_file.Y[i]*scaleY + offsetY, las_file.Z[i]*scaleZ + offsetZ))

    return verts

#creates a mesh of points in blender using .las file
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

#creates a map of cubes in blender using .las file
def plotLASCube(path, size, name="map"):
    #store scene
    scene = bpy.context.scene

    #get vertices
    verts = getVerts(path)

    #store created cubes
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

    #join cubes into one object
    bpy.ops.object.join(ctx)
    
    #relocate and rename the object
    ctx['active_object'].location = [0,0,0]
    ctx['active_object'].name = name


def savePointsLAS(outpath, points):
    if not os.path.isfile(outpath):
        open(outpath, 'a')

    outFile = laspy.file.File(outpath, mode="w", header=inFile.header)
    outFile.points = points

def las2txt(path):
    verts = getVerts(path)
    out = str(len(verts))

    verts = np.array(verts) - np.mean(verts, axis=0)

    for v in verts:
        out += '\n'
        for x in v:
            out += str(np.asscalar(x)) + " "

    open(path[:-3] + "txt", 'a').write(out)

def las2off(path):
    verts = getVerts(path)
    out = "COFF" + '\n' + str(len(verts)) + " 0 0"

    verts = np.array(verts) - np.mean(verts, axis=0)

    for v in verts:
        out += '\n'
        for x in v:
            out += str(np.asscalar(x)) + " "
        out += "0 100 100 100"

    open(path[:-3] + "off", 'a').write(out)