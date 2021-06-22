from boxy import boxy,cif,cwhile
import numpy as np



def t1():
    a=boxy(0.5,1.5)
    a+=1
    print(a)

def t2():
    a=boxy(0.5,1.5)
    b=boxy(5.5,7.5)
    a+=b
    print(a)

def t3():
    a=boxy(0.5,1.5)
    a=cif(a<1,a+1,a+2)
    print(a)

def t4():
    a=boxy(0.5,1.5)
    def inloop(a):
        return {"a":a+3}
    def test(a):
        return a<5
    a=cwhile(test,inloop,a=a)
    print(a)

def t5():
    a=boxy(0.5,1.5)
    def inloop(a):
        return {"a":a+1}
    def test(a):
        return a<5
    a=cwhile(test,inloop,a=a)
    print(a)


t1()

