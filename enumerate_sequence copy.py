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

# print (type(sys.argv[1]))


seq = [int(s) for s in sys.argv[1].split(',')]
print seq

# input X, and output Y
x, y = Bools('x y')

bcSequence = BcSequence(seq, x, y)

bc = bcSequence.getbc()
print bc

bcSequence.find_solution(x, bc)
bcSequence.find_probability()

output = bcSequence.get_output_with_random(x, True, [0, 0, 0])[y]
print bcSequence.transform_bool(output)
