import numpy as np
def convert(h):
    r=list(h.keys())
    r.pop(r.index("dims"))
    dim=h["dims"]
    out=[[0]*int(dim[1]) for i in range(int(dim[0]))]
    for i in r:
        c=[int(k) for k in h[i].keys()]
        for j in c:
            out[int(i)-1][j-1]=h[i][j]
    return np.array(out)
