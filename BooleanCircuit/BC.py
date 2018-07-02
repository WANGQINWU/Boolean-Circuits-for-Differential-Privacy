from z3 import *
from BC_Stat import BCStat


class BcSequence(BCStat):
    r = []

    def __init__(self, sequence, x, y):
        self._sequence = sequence
        self._length = len(self._sequence)
        self.r = self.getri()
        self._output_bc = self.producebc(x, y)
        self._bc = self.for_lie(self._output_bc,x, y)

    def getri(self):

        for i in range(self._length):
            self.r.append(Bool('r%s' % i))
        return self.r

    # Sequence
    def producebc(self, x, y):
        chain_one = x
        chain_two = x

        for i, s in enumerate(self._sequence):
            if s == 0:
                chain_one = Or(chain_one, self.r[i])
                chain_two = And(chain_two, self.r[i])
            else:
                chain_one = And(chain_one, self.r[i])
                chain_two = Or(chain_two, self.r[i])

        chain_one = Not(chain_one)
        chain_two = Not(chain_two)

        bc = self.getmux(x, chain_one, chain_two)

        return bc == y

    def for_lie(self, bc, x, y):
        return bc, y != x

    # Selector
    def getmux(self, x, chain_one, chain_two):
        mux = If(x == False, chain_one, chain_two)
        return mux

    def getbc(self):
        return self._bc

    def get_output_with_random(self, x, input_of_bc, random):
        s = Solver();
        s.add(self._output_bc)
        constraints = And([self.r[i] == self.transform_num(random[i]) for i in range(len(random))])
        constraints = And(constraints, x == input_of_bc)
        s.add(constraints)
        s.check()
        if s.check() == sat:
            return s.model()
        else:
            return 'error'
