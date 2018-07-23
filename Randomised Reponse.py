import sys
from BooleanCircuit.RRclass import RRclass
from z3 import *
from math import *

# accept value from user and return randomised value

print sys.argv

if len(sys.argv) < 2:
    print "please provide value to process"
    exit(0)

value = [int(i) for i in list(sys.argv[1])]
print "before"
print value

# epsilon of differential privacy
epsilon = math.exp(math.log(3))
RR = RRclass(epsilon)

randomized_result = RR.get_results_bit_flip(value)
print "after"
print randomized_result
print

RR.bcSequence.LocalGenRRGOF(0.05, math.log(7), [0, 0, 0, 0, 1], RR)
