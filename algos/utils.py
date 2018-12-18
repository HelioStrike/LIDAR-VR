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