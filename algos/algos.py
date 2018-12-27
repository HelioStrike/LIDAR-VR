#Algos to cover lidar data points in less objects

import numpy as np
import laspy
import os

from utils import *

nodata = ((-99999999,-99999999))


#naive maxpool implementation
def maxpool(data, pool_size, stride=1):
    out = []
    for i in range(0,len(data),stride):
        row = []
        for j in range(0,len(data[0]),stride):
            maxm = -99999999
            for x in range(i,min(i+pool_size, len(data))):
                for y in range(i,min(i+pool_size, len(data))):
                    maxm = max(maxm, data[x][y])
            row.append(maxm)
        out.append(row)
    return out


#given a 2D array, returns rectangles of similar values
def planeGrouping(lidarmap,info):
    maskmap = [[0 for i in range(info["ncols"])] for j in range(info["nrows"])]

    rects = []

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

                rects.append([x1, y1, xs, ys])

                for x2 in range(x1,xs+1):
                    for y2 in range(y1,ys+1):
                        maskmap[x2][y2] = 1

    return rects


#returns distance between (x1,y1,z1) and (x2,y2,z2)
def euclideanDistance(x1,y1,z1,x2,y2,z2):
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5


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