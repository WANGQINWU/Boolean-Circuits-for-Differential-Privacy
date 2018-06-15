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

#define probability
def probability(total, truecount, falsecount, n):

    if(truecount==falsecount):
        print "lie probability for true or false is:"
        print Q(falsecount,n**2)
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
#solve when it lies
s.add(MUX==Y,Y==Not(X))

total=0
tLiecount=0
fLiecount=0
#s.add(Or(R[0]!=m[R[0]],R[1]!=m[R[1]],X!=m[X]))
#print s.check()
#m=s.model()


while s.check() == sat:
    s.check()
    total += 1
    m=s.model()
    print
    #to get multiple solutions and avoid get the same solution all the time
    ORsol= Or([R[i] != m[R[i]] for i in range(len(R))])
    ORsol=Or(ORsol,X!=m[X])
    #print ORsol
    print "solution:"
    print m
    #count lie in when x is true or false
    if m[X]==False:
        fLiecount += 1
    else:
        tLiecount += 1
    print "count of lie:"
    print total
    s.add(ORsol)

#print tLiecount
#print n**2
print float(total)/(n+1)**2

probability(total,tLiecount,fLiecount,n)






