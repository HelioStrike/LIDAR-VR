import laspy
from utils import *
from algos import *


sparsifyLASFile("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_1.las",\
    "/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_50.las",50,50,50)

faces,points = constructFaces("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las",10,10,10)
print(points)

'''
sparsifyLASFile("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las",\
    "/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_10.las",10,10,10)

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las", mode="r")
print(len(inFile.X))

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_25.las", mode="r")
print(len(inFile.X))
'''

'''
inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las", mode="r")
for dim in inFile.point_format:
    print(dim.name)
'''

'''
import bpy
import laspy


nodata = ((-99999999,-99999999))
#numX = maximum number of points in a line along X
#numY = maximum number of points in a line along Y
#numZ = maximum number of points in a line along Z
def sparsify(inpath, numX, numY, numZ):
    inFile = laspy.file.File(inpath, mode="r")
    points = inFile.points

    minX = min(inFile.X)
    minY = min(inFile.Y)
    minZ = min(inFile.Z)
    maxX = max(inFile.X)
    maxY = max(inFile.Y)
    maxZ = max(inFile.Z)
    diffX = maxX - minX
    diffY = maxY - minY
    diffZ = maxZ - minZ

    point_bins = [[[nodata for i in range(numZ+1)] for j in range(numY+1)] \
     for k in range(numX+1)]

    for point in points:
        x_ = int(numX*(point[0][0]-minX)/diffX)
        y_ = int(numY*(point[0][1]-minY)/diffY)
        z_ = int(numZ*(point[0][2]-minZ)/diffZ)
        point_bins[x_][y_][z_] = ((x_*diffX/diffZ,y_*diffY/diffZ,z_),)
        #point_bins[x_][y_][z_] = ((int(x_*(maxX-minX)/numX),int(y_*(maxY-minY)/numY),int(z_*(maxZ-minZ)/numZ)),)

    points = []
    indices = {}
    curr = 0
    for i in range(numX):
        for j in range(numY):
            for k in range(numZ):
                if point_bins[i][j][k] != nodata:
                    points.append(point_bins[i][j][k])
                    indices[str(point_bins[i][j][k])] = curr
                    curr += 1

    return point_bins, points, indices


def constructFaces(inpath, numX, numY, numZ):
    point_bins, points, indices = sparsify(inpath, numX, numY, numZ)
    faces = []

    chek = [[0,1,5,4],[0,1,3,2],[0,2,6,4],[0,1,7,6],[0,2,7,5],[1,3,6,4],[2,3,5,4],[0,3,7,4],[1,2,6,5]]
    
    for x in range(0, numX-1):
        for y in range(0, numY-1):
            for z in range(0, numZ-1):

                cube2 = [-1 for i in range(8)]                
                for x1 in range(2):
                    for y1 in range(2):
                        for z1 in range(2):
                            if point_bins[x+x1][y+y1][z+z1] is not nodata:
                                cube2[x1+y1*2+z1*4] = indices[str(point_bins[x+x1][y+y1][z+z1])]
                            else:
                                cube2[x1+y1*2+z1*4] = -1
                    
                for f in chek:
                    yee = True
                    for p in range(4):
                        if cube2[f[p]] == -1:
                            yee = False
                            break
                    if yee:
                        faces.append((cube2[f[0]],cube2[f[1]],cube2[f[2]],cube2[f[3]]))
    
    return faces, points

faces, points = constructFaces("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las",50,50,50)
name = "wave"
mesh = bpy.data.meshes.new(name)
object = bpy.data.objects.new(name,mesh)
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
pts = []
for point in points:
    pts.append([point[0][0],point[0][1],point[0][2]])
#create mesh from python data
mesh.from_pydata(pts,[],faces)
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
'''