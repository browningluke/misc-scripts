'''
    Simple neural network example for non-linear problems with 1 hidden layer.
    This one here is used to learn the phrase "Hello World!"
'''

import numpy as np
from time import sleep

# Define target string
target = "I want this to be complicated so i am writing a whole sentence here."

# Define activation function
def sigmoid(x, deriv=False):
    if (deriv == True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

# leaky ReLU function
def prelu(x, deriv=False):
    c = np.zeros_like(x)
    slope = 1e-1
    if deriv:
        c[x<=0] = slope
        c[x>0] = 1
    else:
        c[x>0] = x[x>0]
        c[x<=0] = slope*x[x<=0]
    return c

nonlin = sigmoid

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
    l1 = nonlin(np.dot(l0, w0))
    l2 = nonlin(np.dot(l1, w1))

    # print(w1.shape)
    # print(l1.shape)
    # print(l2.shape)

    # Calculate output error
    l2_error = Y - l2

    l2_delta = l2_error * nonlin(l2, True)

    # Calculate layer 1 error
    l1_error = np.dot(l2_delta, w1.T)

    l1_delta = l1_error * nonlin(l1, True)

    # Update weights
    w0 += np.dot(l0.T, l1_delta)
    w1 += np.dot(l1.T, l2_delta)

    # Test
    t0 = np.zeros((dim,dim))
    for j in range(dim):
        t1 = nonlin(np.dot(t0, w0))
        t2 = nonlin(np.dot(t1, w1))
        t0[j+1:,j] = t2[j,0]

    # Print
    chars = np.round(t2.reshape(1,dim)[0] * 128).astype(int)
    string = "".join(chr(c) for c in chars)
    print("\n\n{}\n\n".format(string))
    # sleep(0.0002)

    if string == target:
        #exit()
        break

# Print
t0 = np.zeros((dim,dim))
for j in range(dim):
    t1 = nonlin(np.dot(t0, w0))
    t2 = nonlin(np.dot(t1, w1))
    t0[j+1:,j] = t2[j,0]

chars = np.round(t2.reshape(1,dim)[0] * 128).astype(int)
string = "".join(chr(c) for c in chars)
print("Test: {}".format(string))