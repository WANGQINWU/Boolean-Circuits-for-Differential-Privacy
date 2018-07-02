import sys
from z3 import *
from BooleanCircuit.BC import BcSequence

# usage: python filename.py 0,1,0,....
#                       x->or and or ...-|
#                                        |->Not()->>
#                       x->and or and...-|
# n is number of OR and AND chain size
# result: return synaptic of bc with n OR and AND

# functions
# produce Ri

##############

if len(sys.argv) < 2:
    print "plz enter length for OR and AND chain"
    sys.exit()

# print type(sys.argv[1])

seq = [int(s) for s in sys.argv[1].split(',')]
# print seq

# input X, and output Y

bcSequence = BcSequence(seq)

bc = bcSequence.getbc()
print bc
print

bcSequence.find_solution(bc)
bcSequence.find_probability()

random = [0, 0, 1]
input = 0
output = bcSequence.get_output_with_random(input, random)
print 'output with input 0 and random [0, 0, 1]'
print bcSequence.transform_bool(output)
