import numpy as np
import os
import re


def ReadASCII(full_file_name):
    out = dict()
    if not os.path.exists(full_file_name):
        print("File: %s do not exists:" %(full_file_name))

    with open(full_file_name) as f:
        # header
        header = []
        for line in f.readlines():
            if "# 1:iteration 2:time 3:data" in line:
                header = header + line.split()[1:]
            if "# column format:" in line:
                header = line.split()[3:]
            if "# data columns: " in line:
                del header[-1]
                header = header + line.split()[3:]
                break
        # column name
        names = []
        if len(header) > 0:
            colnum = range(len(header)) 
            for c, name in enumerate(header):
                assert(int(name.split(":")[0]) == c + 1)
                names = names + [name.split(":")[1]] 
    # Get the data
    data = np.loadtxt(full_file_name, comments="#", unpack=True)
    u, indices = np.unique(data[0,:], return_index=True)
    for i , name in enumerate(names):
        out[name] = data[i, indices]
    dim = 0
    return out, dim