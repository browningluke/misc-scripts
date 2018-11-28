'''
    Simple neural network example for non-linear problems with 1 hidden layer.
    This one here is used to learn the phrase "Hello World!"
'''

import numpy as np
from time import sleep

# Define target string
target = "Good day! How are you on this fine evening?"

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
Y = Y.T

np.random.seed(1203)

# Initialize weights, zero centered
w0 = 2 * np.random.random((dim,4)) - 1
w1 = 2 * np.random.random((4,1)) - 1

while True:

    # Forward propagation
    l0 = X
    l1 = sigmoid(np.dot(l0, w0))
    l2 = sigmoid(np.dot(l1, w1))

    # Calculate output error
    l2_error = Y - l2

    l2_delta = l2_error * sigmoid(l2, True)

    # Calculate layer 1 error
    l1_error = np.dot(l2_delta, w1.T)

    l1_delta = l1_error * sigmoid(l1, True)

    # Update weights
    w0 += np.dot(l0.T, l1_delta)
    w1 += np.dot(l1.T, l2_delta)

    # Test
    t0 = np.zeros((dim,dim))
    for j in range(dim):
        t1 = sigmoid(np.dot(t0, w0))
        t2 = sigmoid(np.dot(t1, w1))
        t0[j+1:,j] = t2[j,0]

    # Print
    chars = np.round(t2.reshape(1,dim)[0] * 128).astype(int)
    string = "".join(chr(c) for c in chars)
    print("\n\n{}\n\n".format(string))
    # sleep(0.0002)

    if string == target:
        exit()