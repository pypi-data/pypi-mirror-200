import sys, os
sys.path.append('../elog/')
from elog import logtime, logexc

@logtime
@logexc
def divis(a,b):
    return a/b

def test_timeit():
    divis(10,2)

    try:
        divis(10,0)
    except Exception as e:
        print(e)

test_timeit()