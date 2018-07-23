from z3 import *
import time
import threading
from scipy.stats import chi2

class BCStat():

    def __init__(self):
        self.total_count = 0
        self.t_lie_count = 0
        self.f_lie_count = 0
        self.is_done = False
        self.time = 0
        self.time1 = 0
        self.s = Solver()
        self.s.add(self._output_bc)

    def find_solution(self, constrain, is_time=False):
        self.total_count = 0
        self.t_lie_count = 0
        self.f_lie_count = 0
        self.is_done = False
        # print "start search"
        self.s.push()
        self.s.add(constrain)

        # print "timer"
        start = time.time()

        while self.s.check() == sat and not self.is_done:
            self.s.check()
            self.total_count += 1
            m = self.s.model()
            # print m
            # to get multiple solutions and avoid get the same solution all the time
            try:
                orsol = Or([self.r[i] != m[self.r[i]] for i in range(self._length)
                            if isinstance(m[self.r[i]], type(m[self.x]))])

            except Exception as e:
                print "first line orsol"
                print m
                print orsol
                print(e)

            try:
                orsol = Or(orsol, self.x != m[self.x])
            except Exception as e:
                print "second line orsol"
                print m
                print orsol
                print(e)

            # count lie in when x is true or false
            if not m[self.x]:
                self.f_lie_count += 2 ** (self._length + 2 - len(m))
            else:
                self.t_lie_count += 2 ** (self._length + 2 - len(m))

            self.s.add(orsol)

            if self.s.check() == unsat:
                self.is_done = True

            # for c in s.assertions():
            #    print c
            # print "-----"

        # print "finished search solution"
        end = time.time()
        if is_time:
            self.time1 = end - start
        else:
            self.time = end - start

        self.s.pop()

    def find_solution_thread(self, t_bc, f_bc):
        t1 = threading.Thread(target=self.find_solution, args=(t_bc,))
        is_time = True
        t2 = threading.Thread(target=self.find_solution, args=(f_bc, is_time))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def find_probability(self):
        # print self.f_lie_count
        # print "lie count"
        # print self.t_lie_count

        # if self.t_lie_count == self.f_lie_count:
        # print "lie probability for true or false is:"
        # return Q(self.f_lie_count, 2 ** self._length)
        # return float(self.f_lie_count) / (2 ** self._length)
        if self.f_lie_count >= self.t_lie_count:
            print "f_lie_count"
            print self.f_lie_count
            return float(self.f_lie_count) / (2 ** self._length)
        else:
            print "t_lie_count"
            print self.t_lie_count
            return float(self.f_lie_count) / (2 ** self._length)

    def find_epsilon(self):

        return float(2 ** self._length - self.f_lie_count) / float(self.f_lie_count)

    def transform_num(self, num):
        return {0: False,
                1: True,
                }[num]

    def transform_bool(self, bool):
        if bool:
            return 1
        elif not bool:
            return 0

    def gettime(self):
        if self.time1 < self.time:
            return self.time
        else:
            return self.time1

    def get_total(self):
        return self.f_lie_count*2

    def LocalGenRRGOF(self, alpha, epsilon, input, M_rr):
        output = M_rr.get_results(input)
        print output
        p1 = float(1)/2
        p0 = float(1)/2

        print p1

        p_head_0 = (1/(math.exp(epsilon)+1)) * (math.exp(epsilon)*p0+(1-p0))
        p_head_1 = (1/(math.exp(epsilon)+1)) * (math.exp(epsilon)*p1+(1-p1))
        print p_head_0

        h_head_0 = output.count(0)
        h_head_1 = output.count(1)

        print h_head_0

        q = (h_head_0-len(input)*p_head_0) ** 2 / (len(input)*p_head_0) +\
            (h_head_1-len(input)*p_head_1) ** 2 / (len(input)*p_head_1)

        print (h_head_0-len(input)*p_head_0) ** 2 / (len(input)*p_head_0)

        chi = chi2.isf(q=alpha, df=1)

        if q > chi:
            print "H0 holds fail"
            print q
        else:
            print "H0 holds"
            print q
