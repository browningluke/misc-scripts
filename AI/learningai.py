import numpy as np
from time import sleep

# Define target string
target = "Hello World!"

# Define activation function
def sigmoid(x, deriv=False):
    if (deriv == True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

# Prepare values
values = list(map(lambda c: ord(c) / 128., list(target)))
dim = len(values)

# Build X
X = np.zeros((dim, dim))
for i in range(dim):
        X[i+1:,i] = values[i]

# Build Y
Y = np.zeros((1, dim))
for i in range(dim):
        Y[0,i] = values[i]
print(Y)
Y = Y.T
print(Y)

np.random.seed(1)

# Initialize weights, zero centered
w0 = 2 * np.random.random((dim,4)) - 1
w1 = 2 * np.random.random((4,1)) - 1