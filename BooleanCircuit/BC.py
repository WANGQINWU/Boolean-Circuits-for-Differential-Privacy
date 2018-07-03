from z3 import *
from BC_Stat import BCStat


class BcSequence(BCStat):
    r = []
    # input x and output y
    x, y = Bools('x y')

    def __init__(self, sequence):
        self._sequence = sequence
        self._length = len(self._sequence)
        self.r = self.getri()
        self._output_bc = self.producebc()
        self._bc = self.for_lie(self._output_bc)
        self.t_bc = self.for_t_lie(self._output_bc)
        self.f_bc = self.for_f_lie(self._output_bc)
        BCStat.__init__(self)

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

    def for_lie(self, bc):
        return bc, self.y != self.x

    def for_t_lie(self, bc):
        return bc, self.y != self.x, self.x == True

    def for_f_lie(self, bc):
        return bc, self.y != self.x, self.x == False


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
        s = Solver();

        s.add(self._output_bc)
        constraints = And([self.r[i] == self.transform_num(random[i]) for i in range(len(random))])
        constraints = And(constraints, self.x == self.transform_num(input_of_bc))
        s.add(constraints)
        s.check()
        if s.check() == sat:
            return s.model()[self.y]
        else:
            return 'error'

    def get_outputs(self, intputs_of_bc, randomizer):
        output = []
        for i in intputs_of_bc:
            output.append(self.get_output_with_random(intputs_of_bc[i], randomizer.get_random_seq()))

        return output
