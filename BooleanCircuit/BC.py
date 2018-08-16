import time

from z3 import *
from BC_Stat import BCStat


class BcSequence(BCStat):
    # input x and output y
    x, y = Bools('x y')

    # sequence are info of bc, like [0,0,0,0] -> all OR chain
    def __init__(self, sequence):
        self.r = []

        self._sequence = sequence
        self._length = len(self._sequence)
        self.r = self.getri()
        self._output_bc = self.producebc()
        self._bc = self.for_lie()
        self.t_bc = self.for_t_lie()
        self.f_bc = self.for_f_lie()
        BCStat.__init__(self)
        self.time_get_ans = 0

    # variable for random input
    def getri(self):

        for i in range(self._length):
            self.r.append(Bool('r%s' % i))
        return self.r

    # Sequence
    def producebc(self):
        chain_one = self.x
        chain_two = self.x

        for i, s in enumerate(self._sequence):
            if s == 0:
                chain_one = Or(chain_one, self.r[i])
                chain_two = And(chain_two, self.r[i])
            else:
                chain_one = And(chain_one, self.r[i])
                chain_two = Or(chain_two, self.r[i])

        chain_one = Not(chain_one)
        chain_two = Not(chain_two)

        bc = self.getmux(chain_one, chain_two)

        return bc == self.y

    # constrain for lying, output != input
    def for_lie(self):
        return self.y != self.x

    # constrain for lying, output != input and input=true
    def for_t_lie(self):
        return self.y != self.x, self.x == True

    # constrain for lying, output != input and input=false
    def for_f_lie(self):
        return self.y != self.x, self.x == False

    def getlength(self):
        return self._length

    # Selector
    def getmux(self, chain_one, chain_two):
        mux = If(self.x == False, chain_one, chain_two)
        return mux

    def getbc(self):
        return self._bc

    def get_t_bc(self):
        return self.t_bc

    def get_f_bc(self):
        return self.f_bc

    def get_output_with_random(self, input_of_bc, random):

        self.s.push()
        constraints = And([self.r[i] == self.transform_num(random[i]) for i in range(len(random))])
        constraints = And(constraints, self.x == self.transform_num(input_of_bc))
        self.s.add(constraints)
        self.s.check()

        if self.s.check() == sat:
            y = self.s.model()[self.y]
            self.s.pop()
            return y
        else:
            return 'error'

    def get_outputs(self, intputs_of_bc, randomizer):
        output = []
        for i in range(len(intputs_of_bc)):
            random_seq = randomizer.get_random_seq()

            start = time.time()
            output.append(self.get_output_with_random(intputs_of_bc[i], random_seq))
            end = time.time()

            self.time_get_ans = end - start
        return output

    def get_out_bc(self):
        return self._output_bc
