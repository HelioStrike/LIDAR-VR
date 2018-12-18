import bpy
import math

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

def planeGrouping(lidarmap,info):
    maskmap = [[0 for i in range(info["ncols"])] for j in range(info["nrows"])]

    squares = []

    for x1 in range(0,info["nrows"]):
        for y1 in range(0,info["ncols"]):
            if lidarmap[x1][y1] != info["NODATA_value"] and maskmap[x1][y1] == 0: 
                xs = x1
                ys = y1
                sz = 1
                curr = lidarmap[x1][y1]

                for x2 in range(x1,info["nrows"]):
                    for y2 in range(y1,info["ncols"]):
                        if lidarmap[x2][y2] != curr or maskmap[x1][y1] == 1:
                            break
                    
                    if (x2-x1+1)*(y2-y1+1) < sz:
                        break
                    xs = x2
                    ys = y2
                    sz = (x2-x1+1)*(y2-y1+1)

                squares.append([x1, y1, xs, ys])

                for x2 in range(x1,xs+1):
                    for y2 in range(y1,ys+1):
                        maskmap[x2][y2] = 1

    return squares

verts = []  # the vertex array
faces = []  # the face array


path = "/home/krypt/Downloads/LIDAR-DTM-1M-2014-SP06ne/dtm_F0175425_20141215_20141215_mm_units.asc"
info, lidarmap = loadData(path)

squares = planeGrouping(lidarmap, info)

scaling_factor = 10000
for i in range(info["nrows"]):
    for j in range(info["ncols"]):
        lidarmap[i][j] /= scaling_factor

for s in squares:
    s[2] += 1
    s[3] += 1

    if (s[0],s[1],lidarmap[s[0]][s[1]]) not in verts:
        verts.append((s[0],s[1],lidarmap[s[0]][s[1]]))
    if (s[0],s[3],lidarmap[s[0]][s[3]]) not in verts:
        verts.append((s[0],s[3],lidarmap[s[0]][s[3]]))
    if (s[2],s[1],lidarmap[s[2]][s[1]]) not in verts:
        verts.append((s[2],s[1],lidarmap[s[2]][s[1]]))
    if (s[2],s[3],lidarmap[s[2]][s[3]]) not in verts:
        verts.append((s[2],s[3],lidarmap[s[2]][s[3]]))

    faces.append((verts.index((s[0],s[1],lidarmap[s[0]][s[1]])), verts.index((s[0],s[3],lidarmap[s[0]][s[3]])), \
        verts.index((s[2],s[1],lidarmap[s[2]][s[1]])), verts.index((s[2],s[3],lidarmap[s[2]][s[3]]))))

#create mesh and object
mesh = bpy.data.meshes.new("map")
object = bpy.data.objects.new("map",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)


'''
#Code borrowed from: http://wiki.theprovingground.org/blender-py-mathmesh

# mesh arrays
verts = []  # the vertex array
faces = []  # the face array
 
# mesh variables
numX = 10  # number of quadrants in the x direction
numY = 10  # number of quadrants in the y direction
 
# wave variables
freq = 1  # the wave frequency
amp = 1  # the wave amplitude
scale = 1  #the scale of the mesh

#fill verts array
for i in range (0, numX):
    for j in range(0,numY):
 
        x = scale * i
        y = scale * j
        z = scale*((amp*math.cos(i*freq))+(amp*math.sin(j*freq)))
 
        vert = (x,y,z) 
        verts.append(vert)
 
#fill faces array
count = 0
for i in range (0, numY *(numX-1)):
    if count < numY-1:
        A = i  # the first vertex
        B = i+1  # the second vertex
        C = (i+numY)+1 # the third vertex
        D = (i+numY) # the fourth vertex
 
        face = (A,B,C,D)
        faces.append(face)
        count = count + 1
    else:
        count = 0

#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)
'''