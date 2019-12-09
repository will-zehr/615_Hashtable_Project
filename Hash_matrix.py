import time
import copy
import random
import numpy as np
import sys
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

def play(h):
    r=list(h.keys())
    r.pop(r.index("dims"))
    dim=h["dims"]
    print(dim)
    return type(h)

def convert(h):
    r=list(h.keys())
    r.pop(r.index("dims"))
    dim=h["dims"]
    out=[[0]*int(dim[1]) for i in range(int(dim[0]))]
    for i in r:
        c=[int(k) for k in h[i].keys()]
        for j in c:
            out[int(i)-1][j-1]=h[i][str(j)]
    return np.array(out)

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
    

def main():
    '''i=np.random.choice(range(1,10000000),1000000,replace=True)
    j=np.random.choice(range(1,10000000),1000000,replace=True)
    value=np.random.normal(0,1,1000000)
    dims=[10000000,10000000]
    print("sample done")
    h=hash_matrix(i,j,value,dims)
    aa=multiply(h,h)'''
    '''t1=time.time()
    h1=hash_matrix(i,j,value,dims)
    t2=time.time()
    h3=multiply(h1,h1)
    t3=time.time()
    r=h1.keys()
    t4=time.time()
    d=h1["dims"]
    t5=time.time()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    print(t5-t4)'''
    h=hash_matrix(i=[1,2,3,4],j=[1,2,3,4],value=[9,10,11,12],dims=[10,10])
    h1=hash_matrix(i=[5,5,5,4],j=[1,2,3,8],value=[9,10,11,12],dims=[10,10])
    print(convert(multiply(h,h)))
    return 0

#main()
