import numpy as np
import struct

def parse_images(filename):
    f = open(filename,"rb");
    magic,size = struct.unpack('>ii', f.read(8))
    sx,sy = struct.unpack('>ii', f.read(8))
    X = []
    for i in range(size):
        im =  struct.unpack('B'*(sx*sy), f.read(sx*sy))
        X.append([float(x)/255.0 for x in im]);
    return np.array(X);

def parse_labels(filename):
    one_hot = lambda x, K: np.array(x[:,None] == np.arange(K)[None, :], 
                                    dtype=np.float64)
    f = open(filename,"rb");
    magic,size = struct.unpack('>ii', f.read(8))
    return one_hot(np.array(struct.unpack('B'*size, f.read(size))), 10)

def error(y_hat,y):
    return float(np.sum(np.argmax(y_hat,axis=1) != 
                        np.argmax(y,axis=1)))/y.shape[0]

# helper functions for loss
# this returns a tuple (softmax loss, softmax loss gradient)
softmax_loss = lambda yp,y : (np.log(np.sum(np.exp(yp))) - yp.dot(y), 
                              np.exp(yp)/np.sum(np.exp(yp)) - y)

def get_errors(yp, y, ypt, yt):
    """
    Helper function to compute errors and losses
    
    Arguments:
        yp: 10 x m numpy array of outputs from the classifer
        y: 10 x m numpy array of the true outputs
        ypt: 10 x m numpy array of outputs from the classifer for test data
        yt: 10 x m numpy array of the true outputs for test data
        
    Return:
        (train_err, train_loss, test_err, test_loss)
    """
    train_err = error(yp, y)
    test_err = error(ypt, yt)
    train_loss = sum(softmax_loss(yp[i],y[i])[0] 
                     for i in range(y.shape[0])) / y.shape[0]
    test_loss = sum(softmax_loss(ypt[i],yt[i])[0] 
                    for i in range(yt.shape[0])) / yt.shape[0]
    return (train_err, train_loss, test_err, test_loss)

# function calls to load data
X_train = parse_images("train-images.idx3-ubyte")
y_train = parse_labels("train-labels.idx1-ubyte")
X_test = parse_images("t10k-images.idx3-ubyte")
y_test = parse_labels("t10k-labels.idx1-ubyte")

# print 'No. of training images',X_train.shape[0]
# print 'No. of test images',X_test.shape[0]
##### Implement the functions below this point ######

def grad(Theta, x, y):
    """ 
    Compute the gradient given input x and output y, and current parameters Theta
    Note that this assumes the constant 1 has already been appended to the input
    
    Arguments:
        Theta: 10 x 785 numpy array of current parameters
        x: 785 sized 1D numpy array of input
        y: 10 sized 1D numpy array of output
        
    Return:
        A 10 x 785 numpy array of the gradient
    """
    grad_smax=softmax_loss(np.dot(Theta,x),y)[1]
    grad_smax=grad_smax.reshape(grad_smax.size,1)
    grad=grad_smax*x
    return grad



def softmax_sgd(X, Y, Xt, Yt, epochs=10, alpha = 0.01):

    """ 
    Run stochastic gradient descent to solve linear softmax regression.
    
    Arguments:
        X: numpy array where each row is a training example input of length 784
        y: numpy array where each row is a training output of length 10
        Xt: numpy array of testing inputs
        yt: numpy array of testing outputs
        epochs: number of passes T to make over the whole training set
        alpha: step size
        
    Return:
        A list of tuples (Train Err, Train Loss, Test Error, Test Loss) for each epoch

        These should be computed at the end of each epoch
    """
    #Add bias
    N=X.shape[0]
    z=np.ones((1,N))
    X=np.concatenate((X,z.T),axis=1)
    N=Xt.shape[0]
    z=np.ones((1,N))
    Xt=np.concatenate((Xt,z.T),axis=1)

    #Initialize weight matrix
    W=np.zeros((Y.shape[1],X.shape[1]))
    output=[]

    for _ in xrange(epochs):

        for i in xrange(X.shape[0]):

            X_dat,Y_dat=X[i],Y[i]
            # #Forward pass
            # scores_dat=X[i].dot(W.T)

            #Backward pass
            w_grad=grad(W,X_dat,Y_dat)
            W -= alpha*w_grad

            
        scores_train=X.dot(W.T)
        scores_test=Xt.dot(W.T)
        output.append(get_errors(scores_train,Y,scores_test,Yt))

    return output

# if __name__=="__main__":

#     # function calls to load data
#     X_train = parse_images("train-images.idx3-ubyte")
#     y_train = parse_labels("train-labels.idx1-ubyte")
#     X_test = parse_images("t10k-images.idx3-ubyte")
#     y_test = parse_labels("t10k-labels.idx1-ubyte")

#     print 'No. of training images',X_train.shape[0]
#     print 'No. of test images',X_test.shape[0]

#     print softmax_sgd(X_train,y_train,X_test,y_test)











