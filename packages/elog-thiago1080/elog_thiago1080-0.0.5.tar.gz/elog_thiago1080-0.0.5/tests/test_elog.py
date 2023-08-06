import sys, os
sys.path.append('../elog/')
from elog import logexc

@logexc
def divis(a,b):
    return a/b

def test_elog():
    divis(10,2)

    try:
        divis(10,0)
    except Exception as e:
        print(e)

test_elog()