from boolp import *

def floatlike(q):
    try:
        float(q)
        return True
    except:
        return False


def to_numb(q):
    return boxy(q,q)
def conv(q):
    if floatlike(q):
        q=to_numb(q)
    return q
def overlap(mina,maxa,minb,maxb):
    return ((mina<=minb) and (maxa>=minb)) or ((mina<=maxb) and (mina>=minb)) or ((mina>=minb) and (maxa<=maxb)) or ((mina<=minb) and (maxa>=maxb))



class boxy(object):

    def __init__(s,min,max):
        s.min=float(min)
        s.max=float(max)
        if s.max<s.min:
            s.min,s.max=s.max,s.min

    def __add__(a,b):
        a,b=conv(a),conv(b)
        return boxy(a.min+b.min,a.max+b.max)
    __radd__=__add__
    def __mul__(a,b):
        a,b=conv(a),conv(b)
        return boxy(a.min*b.min,a.max*b.max)
    __rmul__=__mul__
    def __pow__(a,b):
        a,b=conv(a),conv(b)
        return boxy(a.min**b.min,a.max**b.max)
    __rpow__=__pow__
    def __sub__(a,b):
        a,b=conv(a),conv(b)
        return boxy(a.min-b.max,a.max-b.min)
    def __rsub__(a,b):
        a,b=conv(b),conv(a)
        return boxy(a.min-b.max,a.max-b.min)
    def __truediv__(a,b):
        a,b=conv(a),conv(b)
        return boxy(a.min/b.max,a.max/b.min)
    def __rtruediv__(a,b):
        a,b=conv(b),conv(a)
        return boxy(a.min/b.max,a.max/b.min)

    def __abs__(s): 
        return boxy(abs(s.min),abs(s.max))
    def __getattr__(s,w):
        """assumes w is monotonously growing (or simple enough, works for example on __neg__)"""
        def func(*args,**kwargs):
            arg=[conv(zw) for zw in args]
            argmin=[zw.min for zw in arg]
            argmax=[zw.max for zw in arg]
            return boxy(getattr(s.min,w)(*argmin,**kwargs),
                        getattr(s.max,w)(*argmax,**kwargs))
        return func

    def __iter__(s):
        yield s.min
        yield s.max

    def range(s):
        return s.max-s.min

    def __eq__(a,b):
        a,b=conv(a),conv(b)
        if a.range()==0 and b.range()==0 and a.max==b.max:
            return true
        if overlap(*a,*b):
            return possible
        return false

    def __ne__(a,b):
        return notp(a==b)

    def __lt__(a,b):
        a,b=conv(a),conv(b)
        if a.range()==0 and b.range()==0:
            return gobp(a.max<b.max)
        if a.max<b.min:return true
        if a.min>=b.max:return false
        return possible
    def __ge__(a,b):return notp(a<b)
    def __gt__(a,b):
        a,b=conv(a),conv(b)
        if a.range()==0 and b.range()==0:
            return gobp(a.max>b.max)
        if a.min>b.max:return true
        if a.max<=b.min:return false
        return possible
    def __le__(a,b):return notp(a>b)

    def __or__(a,b):
        a,b=conv(a),conv(b)
        mn=min([a.min,b.min])
        mx=max([a.max,b.max])
        return boxy(mn,mx)
    def __and__(a,b):
        a,b=conv(a),conv(b)
        assert overlap(*a,*b),"This is not possible. If you want the intersection of two boxes, those boxes have to overlap"
        mn=max([a.min,b.min])
        mx=min([a.max,b.max])
        return boxy(mn,mx)


    def __repr__(s):
        return f"boxy({s.min},{s.max})"
    def __str__(s):
        return f"[{s.min},{s.max}]"


def cif(test,if_true,if_false):
    if test == true:return if_true
    if test == false:return if_false
    return if_true | if_false


def cwhile(test,loop,**kwargs):
    dic={key:conv(val) for key,val in kwargs.items()}
    while True:
        tes=test(**dic)
        print("Looping with:",dic,"Condition currently",tes)
        if tes is true:
            dic=loop(**dic)
        elif tes is possible:
            ld=loop(**dic)
            for key in ld.keys():
                ld[key]=ld[key]|dic[key]
            dic=ld
        else:
            break
    return dic









