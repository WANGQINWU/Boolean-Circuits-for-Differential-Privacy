from z3 import *


class BCStat():

    total_count = 0
    t_lie_count = 0
    f_lie_count = 0
    s = Solver()

    def find_solution(self, bc):

        self.s.add(bc)

        while self.s.check() == sat:
            self.s.check()
            self.total_count += 1
            m = self.s.model()
            # print m
            # to get multiple solutions and avoid get the same solution all the time
            orsol = Or([self.r[i] != m[self.r[i]] for i in range(self._length) if m[self.r[i]] == True or m[self.r[i]] == False])
            orsol = Or(orsol, self.x != m[self.x])

            # print orsol
            # print "solution:"
            # print m
            # print self.t_lie_count
            # print self.f_lie_count

            # count lie in when x is true or false
            if not m[self.x]:
                self.f_lie_count += 2 ** (self._length + 2 - len(m))
            else:
                self.t_lie_count += 2 ** (self._length + 2 - len(m))
            # print "count of lie:"
            # print self.total_count
            self.s.add(orsol)
            # for c in s.assertions():
            #    print c
            # print "-----"

    def find_probability(self):
        # print self.f_lie_count
        # print self.t_lie_count

        if self.t_lie_count == self.f_lie_count:
            print "lie probability for true or false is:"
            print Q(self.f_lie_count, 2 ** self._length)

    def transform_num(self, num):
        return {0: False,
                1: True,
                }[num]

    def transform_bool(self, bool):
        if bool:
            return 1
        elif not bool:
            return 0
