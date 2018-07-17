import numpy as np

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))


class Network():
    def __init__(self): 
        # input dataset
        self.x = np.array([  [0,0,1],
                        [0,1,1],
                        [1,0,1],
                        [1,1,1] ])
            
        # output dataset            
        self.y = np.array([[0,0,1,1]]).T

        # seed random numbers to make calculation
        # deterministic (just a good practice)
        np.random.seed(1)

        # initialize weights randomly with mean 0
        self.syn0 = 2*np.random.random((3,1)) - 1

    def feedforward(self, a):
        # Return the output of the network for an input vector a
        return nonlin(np.dot(a, self.syn0))

    def backpropogate(self, r):
        for iter in range(r):
            l1 = self.feedforward(self.x)

            # how much did we miss?
            l1_error = self.y - l1

            # multiply how much we missed by the 
            # slope of the sigmoid at the values in l1
            l1_delta = l1_error * nonlin(l1, True)

            # update weights
            self.syn0 += np.dot(self.x.T, l1_delta)

            # test
            t1 = self.feedforward(self.x)
            t = np.round(t1).astype(int)
            if np.array_equal(t, self.y):
                print("Output:")
                print(np.round(t1).astype(int))

    def saveweights(self):
        # Save weights
        print(self.syn0)

def main():
    n = Network()

    n.backpropogate(1000)

    print(np.round(n.feedforward([1,0,1])).astype(int))
    n.saveweights()

if __name__ == '__main__':
    main()
