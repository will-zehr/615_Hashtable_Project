import copy
import numpy as np
def hash_matrix(i,j,value,dims):
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
            h[ind][j[k]]=value[k]
        else:
            h[ind][j[k]]=value[k]
    return h

def plus(h1,h2):
    h3=copy.deepcopy(h2)
    r1=list(h1.keys())
    r1.pop(r1.index("dims"))
    for k in r1:
        if k in h3:
            c=h1[k].keys()
            for j in c:
                if j in h3[k]:
                    h3[k][j]=h3[k][j]+h1[k][j]
                else:
                    h3[k][j]=h1[k][j]
        else:
            h3[k]=copy.deepcopy(h1[k])
    return h3


def multiply(h1,h2):
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
                            h3[i][k]=h3[i][k]+h1[i][j]*h2[j][k]
                        else:
                            h3[i][k]=h1[i][j]*h2[j][k]
                    else:
                        h3[i]=dict()
                        h3[i][k]=h1[i][j]*h2[j][k]
                        
    return h3
