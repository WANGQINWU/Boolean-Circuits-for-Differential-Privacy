import math

from BooleanCircuit.BC import BcSequence
from randomize import Randomize


class RRclass():

    def __init__(self, epsilon):
        self._epsilon = epsilon
        self._length = math.log(self._epsilon + 1, 2)
        self.Randomizer = Randomize(int(self._length))
        self._bcinfo = self.get_bcinfo()
        self.bcSequence = BcSequence(self._bcinfo)

    def get_length_of_bc(self):
        return math.log(self._epsilon + 1, 2)

    def get_bcinfo(self):
        seq = []
        for i in range(int(self._length)):
            seq.append(0)
        return seq

    def get_results(self, input):

        randomized_result = self.bcSequence.get_outputs(input, self.Randomizer)

        result = []
        for i in randomized_result:
            result.append(self.bcSequence.transform_bool(i))
        return result
