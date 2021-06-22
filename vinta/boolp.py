from enum import Enum


class boolp(Enum):
    true=1
    false=-1
    possible=0

true=boolp.true
false=boolp.false
possible=boolp.possible

def gobp(a):
    if a:return true
    return false

def notp(a):
    if a is true:return false
    if a is false:return true
    return a
