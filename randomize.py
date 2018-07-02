import random


class Randomize:

    def __init__(self, length):
        self._length = length

    def get_random_seq(self):
        seq = []

        for i in range(self._length):
            seq.append(random.randint(0, 1))

        return seq
