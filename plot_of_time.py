import math
import time

import matplotlib.pyplot as plt
from BooleanCircuit.RRclass import RRclass
from BooleanCircuit.BC import BcSequence


seq = [0, 0]

x_data = []
y_data = []
y_data2 = []

for i in range(40):
    for j in range(i):
        seq.append(0)
    bcSequence = BcSequence(seq)
    bc = bcSequence.getbc()
    bcSequence.find_solution(bc)
    y_data2.append(bcSequence.find_probability())
    x_data.append(i + 2)
    y_data.append(bcSequence.gettime())
    print i
#
# plt.subplot(1, 1, 1)
# plt.plot(x_data, y_data)
# plt.yscale('log')
# plt.ylabel('time to find solutions')
# plt.xlabel('number of OR gate')

plt.subplot(1, 1, 1)
plt.plot(x_data, y_data2, 'ro', markersize=3)
plt.plot(x_data, y_data2)
plt.yscale('log')
plt.ylabel('probability')
plt.xlabel('number of OR gate')


# x_data1 = []
# y_data1 = []
#
# for i in range(100):
#     epsilon = math.log(2**(i+2)-1)
#     print 2**(i+2)-1
#     RR = RRclass(math.exp(epsilon))
#     print RR.get_length_of_bc()
#     start = time.time()
#     RR.get_bcSequence().LocalGenRRGOF(0.05, epsilon, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], RR)
#     end = time.time()
#     x_data1.append(epsilon)
#     y_data1.append(end - start)
#
# plt.subplot(1, 1, 1)
# plt.plot(x_data1, y_data1, 'ro', markersize=3)
# plt.plot(x_data1, y_data1)
# plt.xscale('log')
# plt.ylabel('time to verification')
# plt.xlabel('epsilon of BC')

plt.show()
