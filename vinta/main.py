from boxy import boxy,cif,cwhile
import numpy as np

from abstr import ordiloop,learn_delta,learn_linear,show_trafos


def golden_ratio(*args):
    x=args[0]
    return (1+1/(abs(x)+0.000001),)

def trivial_sum(x,i):
    return (x+1),

def integer_sum(x,i):
    return (x+i,)

def dual_sum(x,y,i):
    return (x+y,y+1)

def exp(x,val,y,i):
    return (x+(val**i)/y,val,y*(i+1))

def sin_sum(x,i):
    return (x+np.abs(np.sin(np.random.uniform(x.min,x.max))),)

def random_sum(x,i):
    return (x+boxy(0.5,1.5),)


start=boxy(0,1000)
start=boxy(0,1)
start2=boxy(0,1)
steps=1000
steps2=1000#0000

end,trafs=ordiloop(trivial_sum,steps,start)
#end,trafs=ordiloop(integer_sum,steps,start)
#end,trafs=ordiloop(golden_ratio,steps,start)
#end,trafs=ordiloop(dual_sum,steps,start,start2)
#end,trafs=ordiloop(exp,steps,boxy(0,0),start,boxy(1,1))
#end,trafs=ordiloop(sin_sum,steps,start)
#end,trafs=ordiloop(random_sum,steps,start)


show_trafos(trafs)


print("Starting at",start)
print("This results in",*end,f" after {steps} steps")

#method,move=learn_delta(trafs)
#print("extracted a delta of",*move)

method,move=learn_linear(trafs)
#print("extracted a linear function of",*move)

print(f"And after another {steps2} (abstracted) steps this becomes",*method(end,times=steps2))






