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
    chain_one = X
    chain_two = X

    for i,s in enumerate(Sequence):
        if s == 0:
            chain_one=Or(chain_one,R[i])
            chain_two=And(chain_two,R[i])
        else:
            chain_one=And(chain_one,R[i])
            chain_two=Or(chain_two,R[i])

    return (Not(chain_one),Not(chain_two))

#Selector
def getMUX(X,OR,AND):
    MUX = If(X==False,OR,AND)
    return MUX

#define probability
def probability(total, truecount, falsecount, n):

    if(truecount==falsecount):
        print "lie probability for true or false is:"
        print
        print Q(falsecount,2**n)
##############
if(len(sys.argv)<2):
    print "plz enter length for OR and AND chain"
    sys.exit()

#print (type(sys.argv[1]))

seq=[int(s) for s in sys.argv[1].split(',')]
print seq
n=len(seq)
#print type(n)

#Random Ri
R = [ Bool('r%s' % i) for i in range(n) ]
print "printing elements in R"
print R

#R=getRi(n)
#print R

#input X, and output Y
X,Y = Bools('x y')

OR,AND= getSequence(X,R,seq)

MUX=getMUX(X,OR,AND)
print "MUX"
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
    #print m
    #to get multiple solutions and avoid get the same solution all the time
    ORsol= Or([R[i] != m[R[i]] for i in range(len(R)) if m[R[i]]==True or m[R[i]]==False])
    ORsol=Or(ORsol,X!=m[X])

    print ORsol
    print "solution:"
    print m
    #count lie in when x is true or false
    if m[X]==False:
        fLiecount += 2**(len(R)+2-len(m))
    else:
        tLiecount += 2**(len(R)+2-len(m))
    print "count of lie:"
    print total
    s.add(ORsol)
    #for c in s.assertions():
    #    print c
    print "-----"
#print tLiecount
#print n**2
print float(total)/2**(n+1)

probability(total,tLiecount,fLiecount,n)






