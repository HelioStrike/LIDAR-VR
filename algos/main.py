import laspy
from algos import *

'''
sparsifyLASFile("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las",\
    "/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las",100,100,100)

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001.las", mode="r")
print(len(inFile.X))

inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las", mode="r")
print(len(inFile.X))
'''
inFile = laspy.file.File("/home/krypt/Downloads/AK_BrooksCamp_2012_000001/AK_BrooksCamp_2012_000001_rad_100.las", mode="r")
print(inFile.points)
