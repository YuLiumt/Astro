import h5py as h5py
import numpy as np
import re

def ReadHDF5(file, group=''):
    """
    读取 h5 所有数据
    """
    f = h5py.File(file, 'r')
    if len(group) > 0:
       grp = f[group]
    else:
       grp = f
    data = dict()
    for varname in sorted(list(grp)):
        if type(grp[varname]) == h5py._hl.dataset.Dataset:
            data[varname] = np.array(grp[varname])
    f.close()
    dim = 0
    return data, dim

def Import_HDF5_2d(PATH,
     VARs,
     it=0, #initial_time
     rl=0, #refinement_level (0 -> coarser)
     c=0,
     PLANE='xy'):
    """
    读取某层数据
    """
    d = dict()
    for var in VARs:
        filename = "{}/{}.{}.h5".format(PATH, var, PLANE)
        H5d2 = h5py.File(filename, 'r')
        for pippo in list(H5d2):
            pattern = "(\S*)::(\S*) it={} tl=(\d*) rl={} c={}\S*".format(it, rl, c)
            x = re.search(pattern, pippo)
            if x != None:
                print("File:", filename, "Match for", pippo)
                delta = H5d2[pippo].attrs['delta']
                origin = H5d2[pippo].attrs['origin']
                sizeA = H5d2[pippo].shape
                #  if var == "rho":
                #     print "delta= ",delta,"\n origin= ", origin, "\n sizeA[0]= ",sizeA[0], "\n sizeA[1]= ", sizeA[1],"\n"
                d[var] = np.array(H5d2[pippo])
                tmpX = np.arange(0,sizeA[1])*delta[0]+origin[0]
                tmpY = np.arange(0,sizeA[0])*delta[1]+origin[1]
                d[PLANE[0]], d[PLANE[1]] = np.meshgrid(tmpX, tmpY)
        H5d2.close() 
    return d
