import time
import copy
import random
import numpy as np
def hash_matrix(i,j,value,dims):
    i_set=list(set(i))
    j_set=list(set(j))
    h=dict()
    h["dims"]=dims
    h["posi"]=[0 for k in range(len(i))]
    h["r"]=i_set
    h["c"]=j_set
    h["val"]=value
    for k in range(len(i)):
        ind=str(i[k])+","+str(j[k])
        h[ind]=value[k]
        h["posi"][k]=ind

    i_sort_ind=np.argsort(i)
    ite=-1
    for k in i_sort_ind:
        if (ite!=i[k]):
            ite=i[k]
            ind="r"+str(i[k])
            h[ind]=dict()
            h[ind][j[k]]=value[k]
        else:
            h[ind][j[k]]=value[k]
    j_sort_ind=np.argsort(j)
    ite=-1
    for k in j_sort_ind:
        if (ite!=j[k]):
            ite=j[k]
            ind="c"+str(j[k])
            h[ind]=dict()
            h[ind][i[k]]=value[k]
        else:
            h[ind][i[k]]=value[k]
    return h

def plus(h1,h2):
    h3=copy.deepcopy(h2)
    posi1=h1["posi"]
    posi2=h2["posi"]
    for k in posi1:
        if (k in h2):
            h3[k]=h2[k]+h1[k]
            spl=k.split(",")
            h3["r"+spl[0]][int(spl[1])]=h3[k]
            h3["c"+spl[1]][int(spl[0])]=h3[k]
        else:
            h3[k]=h1[k]
            h3["posi"].append(k)
            spl=k.split(",")
            h3["r"].append(int(spl[0]))
            h3["r"]=list(set(h3["r"]))
            h3["c"].append(int(spl[1]))
            h3["c"]=list(set(h3["c"]))
            h3["r"+spl[0]]=dict()
            h3["c"+spl[1]]=dict()
            h3["r"+spl[0]][int(spl[1])]=h1[k]
            h3["c"+spl[1]][int(spl[0])]=h1[k]
    return h3

def multiply(h1,h2):
    ii=[]
    jj=[]
    value=[]
    dims=[h1["dims"][0],h2["dims"][1]]
    for i in h1["r"]:
        key=h1["r"+str(i)].keys()
        jjj=[]
        value2=[]
        for j in key:
            if "r"+str(j) in h2:
                jjj.append([])
                value2.append([])
                key2=h2["r"+str(j)].keys()
                for k in key2:
                    jjj[-1].append(k)
                    value2[-1].append(h1[str(i)+","+str(j)]*h2[str(j)+","+str(k)])
        jj.append([])
        ii.append([])
        value.append([])
        for j in range(len(jjj)):
            for k in range(len(jjj[j])):
                if jjj[j][k] not in jj[-1]:
                    jj[-1].append(jjj[j][k])
                    value[-1].append(value2[j][k])
                    ii[-1].append(i)
                else:
                    value[-1][jj[-1].index(jjj[j][k])]=value[jj[-1].index(jjj[j][k])]+value2[j][k]
    ii1=[]
    jj1=[]
    value1=[]
    [ii1.extend(i) for i in ii]
    [jj1.extend(i) for i in jj]
    [value1.extend(i) for i in value]
        
    h3=hash_matrix(ii1,jj1,value1,dims)
    return h3
    

def main():
    print(1)
    base=[i for i in range(1,10000000)]
    print(2)
    i=random.sample(base,1000000)
    print(3)
    j=random.sample(base,1000000)
    print(4)
    value=np.random.normal(0,1,1000000)
    print(5)
    dims=[10000000,10000000]
    print("*")
    h1=hash_matrix(i,j,value,dims)
    print("**")
    t_start=time.time()
    h3=multiply(h1,h1)
    t_end=time.time()
    print(t_end-t_start)
    '''h=hash_matrix(i=[1,2,3,4],j=[5,6,7,8],value=[9,10,11,12],dims=[10,10])
    h1=hash_matrix(i=[5,5,5,8],j=[1,2,3,4],value=[9,10,11,12],dims=[10,10])
    print(multiply(h,h1))'''
    return 0

#main()
