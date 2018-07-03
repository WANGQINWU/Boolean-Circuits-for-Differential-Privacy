from BooleanCircuit.BC import BcSequence
import matplotlib.pyplot as plt

seq = [0, 0]

x_data = []
y_data = []

x_data1 = []
y_data1 = []
y_data2 = []

seq1 = [0 for i in range(100)]
print seq1

bcSequence1 = BcSequence(seq1)
t_bc1 = bcSequence1.get_t_bc()
bcSequence1.find_solution(t_bc1)

x_data1.append(0)
y_data1.append(bcSequence1.gettime())
y_data2.append(bcSequence1.find_probability())

print type(y_data2[0])

for i in range(98):
    seq1[i + 1] = 1
    print seq1
    bcSequence1 = BcSequence(seq1)
    t_bc1 = bcSequence1.get_t_bc()
    bcSequence1.find_solution(t_bc1)
    x_data1.append(i + 1)
    y_data1.append(bcSequence1.gettime())
    y_data2.append(float(bcSequence1.find_probability()))
    print i

for i in range(98):
    for j in range(i):
        seq.append(0)
    bcSequence = BcSequence(seq)
    bc = bcSequence.getbc()
    bcSequence.find_solution(bc)
    x_data.append(i + 2)
    y_data.append(bcSequence.gettime())
    print i

plt.subplot(3, 1, 1)
plt.plot(x_data, y_data, 'ro')
plt.axis([1, 100, 0, max(y_data)])
plt.ylabel('time to find solutions')
plt.xlabel('number of OR gate')

# plt.xticks(x_data, [str(i) for i in x_data])

plt.subplot(3, 1, 2)
plt.plot(x_data1, y_data1, 'ro')
plt.axis([1, 100, 0, max(y_data1)])
plt.ylabel('time to find probability')
plt.xlabel('number of AND in 100 gate')

# plt.xticks(x_data1, [str(i) for i in x_data1])

plt.subplot(3, 1, 3)
plt.plot(x_data1, y_data2, 'ro')
plt.axis([1, 100, 0, max(y_data2)])
plt.ylabel('probability of lying')
plt.xlabel('number of AND in 100 gate')

plt.show()
