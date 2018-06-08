from z3 import *
import sys

#functions
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
    for i in range(2):
        OR=Or(OR,R[i])
    return Not(OR)

#AND chain
def getAND(X,R,n):
    AND=X
    for i in range(2):
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

print(sys.argv[1:])

R = [ Bool('r%s' % i) for i in range(2) ]
print "printing elements in R"
print R

X,Y = Bools('x y')

print "printing elements in OR"
OR=getOR(X,R,2)
print OR

print "printing elements in AND"
AND=getAND(X,R,2)
print AND

print "printing elements in MUX"
MUX=getMUX(X,OR,AND)
print MUX

s = Solver()
s.add(MUX==Y,X==False,R[0]==False,R[1]==False)

s.check()
m = s.model()
print m

#X=True
R[0]=False
R[1]=False

OR=getOR(X,R,2)
AND=getAND(X,R,2)
MUX=getMUX(X,OR,AND)

statement=(MUX==Not(X))

proveforall(statement)
proveforall(OR==Not(X))
