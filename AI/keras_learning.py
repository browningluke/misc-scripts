# Larger CNN for the MNIST Dataset
import numpy
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

from PIL import Image
img = Image.open('two.png').convert('L')
arr = numpy.array(img)
print(arr.shape)
arr = arr.reshape(1, 1, 28, 28).astype('float32')
print(arr.shape)

model = load_model('model1.h5')

prediction = model.predict(arr, verbose=2)[0]
bestclass = ''
bestconf = -1
for n in [0,1,2,3,4,5,6,7,8,9]:
    if (prediction[n] > bestconf):
        bestclass = str(n)
        bestconf = prediction[n]
print('I think this digit is a ' + bestclass + ' with ' + str(bestconf * 100) + '% confidence.')