from z3 import *
import time
import threading


class BCStat():

    def __init__(self):
        self.total_count = 0
        self.t_lie_count = 0
        self.f_lie_count = 0
        self.is_done = False
        self.time = 0
        self.time1 = 0
        self.mutex = threading.Lock()

    def find_solution(self, bc, is_time=False):

        # print "start search"
        s = Solver()
        s.add(bc)

        # print "timer"
        start = time.time()

        while s.check() == sat and not self.is_done:
            s.check()
            self.total_count += 1
            m = s.model()
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

            s.add(orsol)

            if s.check() == unsat:
                self.mutex.acquire()
                self.is_done = True
                self.mutex.release()

            # for c in s.assertions():
            #    print c
            # print "-----"

        # print "finished search solution"
        end = time.time()
        if is_time:
            self.time1 = end - start
        else:
            self.time = end - start

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
            # print self.f_lie_count
            return float(self.f_lie_count) / (2 ** self._length)
        else:
            # print self.t_lie_count
            return float(self.t_lie_count) / (2 ** self._length)

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
