from utils import *
from algos import *

path = "../data/LIDAR-DTM-1M-2014-SP06ne/dtm_F0175425_20141215_20141215_mm_units.asc"
info, lidarmap = loadData(path)

squares = planeGrouping(lidarmap, info)
print(squares[:10])
print(len(squares))

data = maxpool(lidarmap,20,20)
info["nrows"] = len(data)
info["ncols"] = len(data[0])

squares = planeGrouping(data, info)
print(squares[:10])
print(len(squares))