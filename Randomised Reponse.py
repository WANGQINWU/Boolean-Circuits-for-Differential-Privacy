import sys
from BooleanCircuit.BC import BcSequence
from z3 import *
from randomize import Randomize
from math import *

# accept value from user and return randomised value

print sys.argv

if len(sys.argv) < 2:
    print "please provide value to process"
    exit(0)

value = [int(i) for i in list(sys.argv[1])]
print value

# epsilon of differential privacy
epsilon = math.exp(math.log(7))

length_of_bc = math.log(epsilon + 1, 2)
randomizer = Randomize(int(length_of_bc))

print "length of boolean circuits is "
print length_of_bc

seq = []

for i in range(int(length_of_bc)):
    seq.append(0)

print seq

bcSequence = BcSequence(seq)

randomized_result = bcSequence.get_outputs(value, randomizer)
print randomized_result
