import copy
import numpy as np
def hash_matrix_tc(i,j,dims):
    i_set=list(set(i))
    j_set=list(set(j))
    h=dict()
    h["dims"]=dims
    i_sort_ind=np.argsort(i)
    ite=-1
    for k in i_sort_ind:
        if (ite!=i[k]):
            ite=i[k]
            ind=i[k]
            h[ind]=dict()
            h[ind][j[k]]=1
        else:
            h[ind][j[k]]=1
    return h



def multiply_tc(h1,h2):
    h3=dict()
    h3["dims"]=[h1["dims"][0],h2["dims"][1]]
    r1=list(h1.keys())
    r1.pop(r1.index("dims"))
    for i in r1:
        key=h1[i].keys()
        for j in key:
            if j in h2:
                key2=h2[j].keys()
                for k in key2:
                    if(i in h3):
                        if(k in h3[i]):
                            h3[i][k]=1
                        else:
                            h3[i][k]=1
                    else:
                        h3[i]=dict()
                        h3[i][k]=1
    return h3
    
def transitive_closure(adj):
    while True:
        adj1=multiply_tc(adj,adj)
        if adj==adj1:
            break
        else:
            adj=adj1
    return adj
