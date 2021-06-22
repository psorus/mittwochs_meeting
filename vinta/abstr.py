from boxy import boxy,conv,cif,cwhile
import numpy as np
from plt import *

def ordiloop(func,times,*args):
    x=[conv(zw) for zw in args]

    trafos=[]

    for i in range(times):
        nx=func(*x,i)
        trafos.append({"inn":[zw for zw in x],"out":[zw for zw in nx]})
        x=nx
    return x,trafos

def conv_trafos(trafos,shall2d=True):
    inn=[[[*zx] for zx in zw["inn"]] for zw in trafos]
    out=[[[*zx] for zx in zw["out"]] for zw in trafos]
    inn=np.array(inn)
    out=np.array(out)
    #print(inn.shape,out.shape)

    if shall2d:
        return make2d(inn),make2d(out)
    else:
        return inn,out

def show_trafos(trafos):
    inn,out=conv_trafos(trafos,shall2d=False)
    par=int(inn.shape[1])
    for i in range(par):
        mn=inn[:,i,0]
        mx=inn[:,i,1]
        x=np.arange(len(mn))
        plt.plot(x,mn,label=f"minima {i}",alpha=0.5)
        plt.plot(x,mx,label=f"maxima {i}",alpha=0.5)
    plt.legend()
    #plt.yscale("log",nonpositive="clip")
    plt.show()

def make2d(arr):
    arr=np.array(arr)
    return arr.reshape((arr.shape[0],int(np.prod(arr.shape[1:]))))
def make3d(arr):
    """actually makes the array 2d sometimes"""
    if len(arr.shape)==2:
        arr=np.array(arr)
        return np.reshape(arr,(arr.shape[0],int(arr.shape[0]/2),2))
    else:
        arr=np.array(arr)
        return np.reshape(arr,(int(arr.shape[0]/2),2))
def goboxy(arr):
    return [boxy(*zw) for zw in arr]



def running_mean(q,alpha=0.9):
    val=q[0]
    for zw in q[1:]:
        val=val*alpha+zw*(1-alpha)
    return val

def learn_delta(trafos):
    inn,out=conv_trafos(trafos)
    delta=out-inn
    rdelta=make3d(running_mean(delta))
    move=goboxy(rdelta)
    def func(x,move=move,times=1):
        return [zx+zm*times for zx,zm in zip(x,move)]
    return func,move


def learn_linear(trafos):
    inn,out=conv_trafos(trafos,shall2d=False)
    delta=out-inn
    numpa=int(delta.shape[1])
    #print(delta.shape)
    #exit()
    x=np.arange(len(delta))
    lin=[[list(np.polyfit(x,delta[:,j,i],1)) for i in range(2)] for j in range(numpa)]
    #print(lin)
    deltas=[]
    consts=[]
    for slin in lin:
        delta,const=[boxy(mn,mx) for mn,mx in zip(*slin)]
        deltas.append(delta)
        consts.append(const)
    def func(x,i=1000,deltas=deltas,consts=consts,times=1):
        """
            +const+delta*i
            +const+delta*(i+1)
            ...
            +const+delta*(i+times-1)

            =

            +times*const+((i+times-1)*(i+times-2)-i*(i-1))/2

            =

            +times*const
            -(i-i-times+1-1)*(i+i+times-1)/2

            =

            +times*const
            +times*(2*i+times-1)/2

            =

            +times*(const+i+times/2-1/2)


        """
        return [zx+times*(const+delta*(i+times/2-1/2)) for zx,const,delta in zip(x,consts,deltas)]
    return func,(deltas,consts)




