import abc
import math
import numpy as np
import scipy.io as spio
from scipy.misc import imread
from scipy.misc import imresize

def argmax(collection):
  """
  Returns a tuple, (argmax, max), containing the index at which the greatest
  value is found in collection, argmax, and the value at that index, max.
  """
  return max(enumerate(collection), key=lambda x: x[1])

# CNN Framework ################################################################

class Cnn(object):

  def __init__(self):
    # layers is a list of CnnLayer objects
    self.layers = []

  def load(self, matFile):
    matData = spio.loadmat(matFile)

    # Read the metadata.
    self.classes = matData['meta'][0][0][0][0][0][1][0]

    self.averageImage = matData['meta'][0][0][1][0][0][0]
    self.imageSize = matData['meta'][0][0][1][0][0][3][0]

    # Read the layers.
    for layer in range(0, matData['layers'][0].size):
      layerObject = matData['layers'][0][layer][0][0]
      layerType = layerObject[1][0]
      print(layerType)
      if layerType == 'conv':
        self.layers.append(ConvLayer(
          layerObject[2][0][0], 
          layerObject[2][0][1], 
          layerObject[5][0][0], 
          layerObject[4][0]))
      if layerType == 'relu':
        self.layers.append(ReluLayer())
      if layerType == 'pool':
        self.layers.append(PoolLayer(
          layerObject[3][0], 
          layerObject[4][0][0], 
          layerObject[5][0]))
      if layerType == 'lrn':
        self.layers.append(NormalizationLayer(
          layerObject[2][0][0],
          layerObject[2][0][1],
          layerObject[2][0][2],
          layerObject[2][0][3]))
      if layerType == 'softmax':
        self.layers.append(SoftmaxLayer())

    # Return self to enable chaining.
    return self


  def classify(self, imageFile):

    # Read the image file and pre-process it to make it suitable for the CNN by
    # scaling the image to be the right size and subtracting the average image.
    im = imread(imageFile)
    im = imresize(im, (self.imageSize[0], self.imageSize[1])).astype(float)
    im -= self.averageImage

    # The feature maps are initialized to the original image.
    featureMaps = im

    # Process all the layers.
    for layer in self.layers:
      featureMaps = layer.processLayer(featureMaps)

    # Return the top class and confidence.
    flattenedResult = [x \
      for maps in featureMaps \
        for y in maps \
          for x in y]
    result = argmax(flattenedResult)

    print(self.classes[result[0]])

    return result


class CnnLayer(object):

  def __init__(self, layerType):
    self.layerType = layerType

  @abc.abstractmethod
  def processLayer(self, prevLayer):
    """
    Given the feature maps from the previous layer, returns the output of this 
    layer.
    """
    return


class ConvLayer(CnnLayer):

  def __init__(self, filters, biases, stride, pad):
    CnnLayer.__init__(self, "conv")
    self.filters = filters
    self.biases = biases
    self.stride = stride
    self.pad = pad

  def processLayer(self, prevLayer):
    """
    TODO: implement this.

    filters is an (n x n x d1 x d2) numpy array where n is the filter size, d1
    is the number of incoming feature maps, and d2 is the number of output
    feature maps.

    biases is a size d2 numpy array with one bias value to be added to each of
    the output feature maps.

    stride is an integer indicating the stride size in both the x and y
    direction.

    pad is a (4 x 1) numpy array with the paddings [top, bottom, left, right].
    """
    stride=self.stride
    out_layer=None
    leng,bread,dept=prevLayer.shape
    top,bottom,left,right=self.pad
    fil_len,fil_bre,fil_dep,fil_out=self.filters.shape
    out_leng,out_bread,out_dept=math.floor((top+bottom+leng-fil_len)/stride)+1,math.floor((left+right+bread-fil_bre)/stride)+1,fil_out
    out_layer_pass=np.zeros((out_leng,out_bread,out_dept))
    ##Pad the incoming feature map##
    left_zeros=np.zeros((leng,left,dept))
    out_layer=np.concatenate((left_zeros,prevLayer),axis=1)
    right_zeros=np.zeros((leng,right,dept))
    out_layer=np.concatenate((out_layer,right_zeros),axis=1)
    leng,bread,dept=out_layer.shape
    top_zeros=np.zeros((top,bread,dept))
    out_layer=np.concatenate((top_zeros,out_layer),axis=0)
    bottom_zeros=np.zeros((bottom,bread,dept))
    out_layer=np.concatenate((out_layer, bottom_zeros),axis=0)  

    ##Forward Pass##
    for i in xrange(int(out_dept)):
      for j in xrange(int(out_bread)):
        for k in xrange(int(out_leng)):
          out_layer_pass[k,j,i]=np.sum(self.filters[:,:,:,i]*out_layer[k*stride:k*stride+fil_len,j*stride:j*stride+fil_bre,:]) + self.biases[i]



    return out_layer_pass




class PoolLayer(CnnLayer):

  def __init__(self, size, stride, pad):
    CnnLayer.__init__(self, "pool")
    self.size = size
    self.stride = stride
    self.pad = pad

  def processLayer(self, prevLayer):
    """
    TODO: implement this.

    size is a (2 x 1) numpy array with the dimensions of the receptive field of
    the pooling operation.

    stride is an integer indicating the stride size in both the x and y
    direction.

    pad is a (4 x 1) numpy array with the paddings [top, bottom, left, right].
    """
    stride=self.stride
    out_layer=None
    leng,bread,dept=prevLayer.shape
    top,bottom,left,right=self.pad
    fil_len,fil_bre=self.size
    out_leng,out_bread,out_dept=math.floor((top+bottom+leng-fil_len)/stride)+1,math.floor((left+right+bread-fil_bre)/stride)+1,dept
    out_layer_pass=np.zeros((out_leng,out_bread,out_dept))
    ##Pad the incoming feature map##
    left_zeros=np.zeros((leng,left,dept))
    out_layer=np.concatenate((left_zeros,prevLayer),axis=1)
    right_zeros=np.zeros((leng,right,dept))
    out_layer=np.concatenate((out_layer,right_zeros),axis=1)
    leng,bread,dept=out_layer.shape
    top_zeros=np.zeros((top,bread,dept))
    out_layer=np.concatenate((top_zeros,out_layer),axis=0)
    bottom_zeros=np.zeros((bottom,bread,dept))
    out_layer=np.concatenate((out_layer, bottom_zeros),axis=0)  

    ##Implement maxpooling##
    for i in xrange(int(out_dept)):
      for j in xrange(int(out_bread)):
        for k in xrange(int(out_leng)):
          out_layer_pass[k,j,i]=np.max(out_layer[k*stride:k*stride+fil_len,j*stride:j*stride+fil_bre,i])

    return out_layer_pass



class ReluLayer(CnnLayer):

  def __init__(self):
    CnnLayer.__init__(self, "relu")

  def processLayer(self, prevLayer):
    """
    TODO: implement this.
    """
    return np.maximum(prevLayer,0)


class SoftmaxLayer(CnnLayer):

  def __init__(self):
    CnnLayer.__init__(self, "softmax")

  def processLayer(self, prevLayer):
    """
    TODO: implement this.
    """
    #prevLayer=prevLayer.reshape(prevLayer.shape[2],-1)

    return np.exp(prevLayer)/np.sum(np.exp(prevLayer))


class NormalizationLayer(CnnLayer):

  def __init__(self, n, kappa, alpha, beta):
    CnnLayer.__init__(self, "normalize")
    self.n = n
    self.kappa = kappa
    self.alpha = alpha
    self.beta = beta

  def processLayer(self, prevLayer):
    """
    TODO: implement this.
    """
    summ=None
    d=prevLayer.shape[2]
    out_layer=np.zeros_like(prevLayer)
    for i in xrange(prevLayer.shape[0]):
      for j in xrange(prevLayer.shape[1]):
        for k in xrange(prevLayer.shape[2]):
          summ=np.sum((prevLayer[i,j,max(0,k-math.floor((self.n-1)/2)):min(d,k+math.ceil((self.n-1)/2))]**2))
          out_layer[i,j,k]=prevLayer[i,j,k]/(self.kappa+self.alpha*summ)

    return out_layer



if __name__=='__main__':

  filters=np.ones((3,3,4,6))
  stride=1
  biases=np.ones(6)
  layer=SoftmaxLayer()
  prevLayer=np.random.uniform(0,5,(1,1,4))
  print prevLayer,'------------------------------'
  print layer.processLayer(prevLayer)