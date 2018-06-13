from z3 import *
import sys

#usage: python filename.py n
# n is number of OR and AND chain size
#result: return synatic of bc with n OR and AND

#functions
#produce Ri
def getRi(n):
    R=[]
    for i in range(n):
        R.append(Bool('r%s' % i))
    return R

# statement p always true, not p always false (unsat)
def proveforall(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        print "proved"
    else:
        print "failed to prove"

#OR chain
def getOR(X,R,n):
    OR=X
    for i in range(n):
        OR=Or(OR,R[i])
    return Not(OR)

#AND chain
def getAND(X,R,n):
    AND=X
    for i in range(n):
        AND=And(AND,R[i])
    return Not(AND)

#Sequence
def getSequence(X,R,Sequence):
    chain = X
    for i,s in enumarte(Sequence):
        if s == 0:
            chain=Or(chain,R[i])
        else:
            chain=And(chain,R[i])

#Selector
def getMUX(X,OR,AND):
    MUX = If(X==False,OR,AND)
    return MUX
##############

if(len(sys.argv)<2):
    print "plz enter length for OR and AND chain"
    sys.exit()

#print (type(sys.argv[1]))
n=int(sys.argv[1])
print type(n)

#Random Ri
R = [ Bool('r%s' % i) for i in range(n) ]
print "printing elements in R"
print R

#R=getRi(n)
#print R

#input X, and output Y
X,Y = Bools('x y')

OR=getOR(X,R,n)

AND=getAND(X,R,n)

MUX=getMUX(X,OR,AND)
print MUX

s=Solver()
s.add(MUX==Y,Y==Not(X))
s.check()
m=s.model()
print m

