import numpy as np
import random

class NeuralNetwork:
    def __init__(self, fileName, layers=[10, 6, 1]):
        layers[0] += 1
        self.layers = layers
        self.w = [np.random.rand(layers[0], layers[1]), np.random.rand(layers[1], layers[2])]
        file = open(fileName, 'r')
        self.input = list()
        self.output = list()
        for line in file:
            line = [float(x) for x in line.strip().split()]
            line.insert(layers[0] - 1, 1)
            self.input.append(line[:layers[0]])
            self.output.append(line[layers[0]])
        # self.output = [0 if x == 2 else 1 for x in self.output]
        maxOut = max(self.output)
        self.output = [x/maxOut for x in self.output]
        self.output = [0 if x == 0.5 else x for x in self.output]
        self.maxIn = [max([x[i] for x in self.input]) for i in range(len(self.input[0]))]
        self.input = [[x[i]/self.maxIn[i] for i in range(len(self.input[0]))] for x in self.input]
        self.output = np.array(self.output).reshape(len(self.output), 1)

    def sigmoidFunction(self, x):
        return 1/(1+np.exp(-x))

    def sigmoidFunctionPrime(self, x):
        return np.exp(-x)/((1+np.exp(-x))**2)

    def gausianFunction(self, x):
        return 1/(1+x**2)

    def gausianFunctionPrime(self, x):
        return -(2*x)/((1+x**2)**2)

    def forwardPropagation(self):
        self.a = np.matmul(self.input, self.w[0])  # pass the input layer through the first set of weights to the second layer
        self.b = [[self.gausianFunction(x) for x in y] for y in self.a]  # apply the activation function to the second layer
        self.c = np.matmul(self.b, self.w[1])  # pass the second layer through the second set of weights to the third layer (output)
        self.d = [[self.sigmoidFunction(x) for x in y] for y in self.c]  # apply the activation function to the output

        return self.d

    def singleForwardPropogation(self, input, scale=False):

        if scale:
            input = [input[i]/self.maxIn[i] for i in range(len(self.maxIn))]

        a = [0] * self.layers[1]
        for i in range(self.layers[0]):
            for j in range(self.layers[1]):
                a[j] += input[i] * self.w[0][i][j]

        for i in range(len(a)):
            a[i] = self.sigmoidFunction(a[i])

        c = [0] * self.layers[2]
        for i in range(self.layers[1]):
            for j in range(self.layers[2]):
                c[j] += a[i] * self.w[1][i][j]

        for i in range(len(c)):
            c[i] = self.sigmoidFunction(c[i])

        """a = [sum([self.w[0][i][j] * input[i] for i in range(self.layers[0])]) for j in range(self.layers[1])]  # pass the input layer through the first set of weights to the second layer
        b = [self.gausianFunction(x) for x in a]  # apply the activation function to the second layer
        c = [sum([self.w[0][i][j] * b[i] for i in range(self.layers[1])]) for j in range(self.layers[2])]  # pass the second layer through the second set of weights to the third layer (output)
        d = [self.sigmoidFunction(x) for x in c]  # apply the activation function to the output"""
        return c

    def backPropagation(self):
        estimate = self.forwardPropagation()
        error = np.subtract(self.output, estimate)

        delta3 = np.multiply(np.multiply(-1, error), [[self.gausianFunctionPrime(x) for x in y] for y in self.c])
        dJdW2 = np.matmul(np.array(self.b).T, delta3)

        delta2 = np.multiply(np.matmul(delta3, np.array(self.w[1]).T), [[self.sigmoidFunctionPrime(x) for x in y] for y in self.a])
        dJdW1 = np.matmul(np.array(self.input).T, delta2)

        descentScalar = 0.01
        self.w[0] = np.subtract(self.w[0], np.multiply(descentScalar, dJdW1))
        self.w[1] = np.subtract(self.w[1], np.multiply(descentScalar, dJdW2))
        # print(dJdW1, dJdW2)

    def getCost(self):
        return np.sum(np.dot(0.5, np.square(np.subtract(self.output, self.forwardPropagation()))))

    def getPercentCorrect(self):
        estimate = nn.forwardPropagation()
        return sum([1 if round(estimate[i][0]) == nn.output[i] else 0 for i in range(len(estimate))])/len(nn.output)

    """def getLayers(self):
        return self.layers

    def getNetwork(self):
        return self.w

    def setNetwork(self, w):
        self.w = w"""

    def loadNetwork(self, file):
        f = open(file, 'r')
        for i in range(2):
            for j in range(self.layers[i]):
                self.w[i][j] = [float(x) for x in f.readline().split()]

    def printNetwork(self):
        for i in range(2):
            for j in range(self.layers[i]):
                for k in range(self.layers[i + 1]):
                    print(self.w[i][j][k], end=' ')
                print("")

    def randomize(self, randNumber=(1, 1), randRange=1):
        s = self.layers[0] * self.layers[1]
        temp1 = random.randint(randNumber[0], randNumber[1])
        for _ in range(temp1):
            i = random.randint(0, s + self.layers[1] * self.layers[2] - 1)
            if i < s:
                self.w[0][int(i/self.layers[1])][i%self.layers[1]] += (random.random() * 2 - 1) * randRange
            else:
                i -= s
                self.w[1][int(i/self.layers[2])][i%self.layers[2]] += (random.random() * 2 - 1) * randRange


if __name__ == '__main__':
    nn = NeuralNetwork("logFile.txt", [4, 3, 1])
    nn.loadNetwork('network.txt')
    #print(nn.getCost(), nn.getPercentCorrect())
    #cost = nn.getCost()
    #w = nn.w
    #print(cost)
    #print(nn.getPercentCorrect())
    """for i in range(1000):
        nn.randomize()
        cost2 = nn.getCost()
        if cost2 > cost:
            nn.w = w
        else:
            print("changed", i)
            cost = cost2
            w = nn.w
        print(cost)"""
    """for i in range(500):
        if i%50 == 0:
            nn.printNetwork()
            print("")
            print(i, nn.getPercentCorrect(), nn.getCost())
            print("")
        nn.backPropagation()
    print(nn.getCost())
    print(nn.getPercentCorrect())
    nn.printNetwork()"""
