import laspy

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

def consolify(path):
    return '\n'.join([d for d in open(path).read().split('\n') if d is not ''])

def plotLAS(path, name):
    las_file = laspy.file.File(path, mode="r")

    #vertices array
    verts = []

    # scaling factors
    scaleX, scaleY, scaleZ = las_file.header.scale
    offsetX, offsetY, offsetZ = las_file.header.offset

    for i in range(len(las_file.X)):
        verts.append((las_file.X[i]*scaleX + offsetX, las_file.Y[i]*scaleY + offsetY, las_file.Z[i]*scaleZ + offsetZ))

    #create mesh and object
    mesh = bpy.data.meshes.new(name)
    object = bpy.data.objects.new(name,mesh)
    
    #set mesh location
    object.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(object)
    
    #create mesh from python data
    mesh.from_pydata(verts,[],[])
