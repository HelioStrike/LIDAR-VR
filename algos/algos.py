#Algos to cover lidar data points in less objects

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