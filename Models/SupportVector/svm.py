"""Support Vector Machine (SVM) model."""

import numpy as np
import math


class SVM:
    def __init__(self, n_class: int, lr: float, epochs: int, reg_const: float):
        """Initialize a new classifier.

        Parameters:
            n_class: the number of classes
            lr: the learning rate
            epochs: the number of epochs to train for
            reg_const: the regularization constant
        """
        self.w = None  # TODO: change this #haha nope.
        self.alpha = lr
        self.epochs = epochs
        self.reg_const = reg_const
        self.n_class = n_class

    def calc_gradient(self, X_train: np.ndarray, y_train: np.ndarray) -> np.ndarray:
        """Calculate gradient of the svm hinge loss.

        Inputs have dimension D, there are C classes, and we operate on
        mini-batches of N examples.

        Parameters:
            X_train: a numpy array of shape (N, D) containing a mini-batch
                of data
            y_train: a numpy array of shape (N,) containing training labels;
                y[i] = c means that X[i] has label c, where 0 <= c < C

        Returns:
            the gradient with respect to weights w; an array of the same shape
                as w
        """

        things = sum((self.w * X_train).transpose())
        #print("computed things")
        #print(things.shape)
        losses = things*y_train
        #print(losses)
        #print(losses.shape)
        g = np.less(losses,1) #select only items with hinge loss > 0


        yixig = ( y_train * X_train.transpose() *g ).transpose()
        #print(yixig.shape)



        ret = self.w - self.reg_const*sum(yixig)



        return ret

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the classifier.

        Hint: operate on mini-batches of data for SGD.

        Parameters:
            X_train: a numpy array of shape (N, D) containing training data;
                N examples with D dimensions
            y_train: a numpy array of shape (N,) containing training labels
        """

        temp = np.zeros((X_train.shape[0],X_train.shape[1]+1)).astype(np.longdouble)
        for i in range(len(X_train)):
            temp[i] = np.append(X_train[i],1)

        X_train = temp


        if self.w is None:
            self.w = np.zeros((X_train.shape[1]))

        batch_size = 20


        batches = X_train.shape[0] // batch_size
        for n in range(self.epochs):
            for old_index in range(len(X_train)):
                new_index = np.random.randint(old_index+1)
                X_train[old_index] , X_train[new_index] = X_train[new_index], X_train[old_index]
                y_train[old_index] , y_train[new_index] = y_train[new_index], y_train[old_index]
            for i in range(batches+1):
                x_sub = X_train[i*batch_size:(i+1)*batch_size]
                y_sub = y_train[i*batch_size:(i+1)*batch_size]
                self.w -= self.alpha * self.calc_gradient(x_sub,y_sub)




        return

    def train_one(self,X_train:np.ndarray,y_train:np.ndarray):

        temp = np.zeros((X_train.shape[0],X_train.shape[1]+1)).astype(np.longdouble)
        for i in range(len(X_train)):
            temp[i] = np.append(X_train[i],1)

        X_train = temp

        #shuffling because... apparently important.
        #rng = np.random.default_rng() #this only contains the rand generators...
        for old_index in range(len(X_train)):
            new_index = np.random.randint(old_index+1)
            X_train[old_index] , X_train[new_index] = X_train[new_index], X_train[old_index]
            y_train[old_index] , y_train[new_index] = y_train[new_index], y_train[old_index]

        if self.w is None:
            self.w = np.zeros((X_train.shape[1]))


        batch_size = 20

        batches = X_train.shape[0] // batch_size
        for i in range(batches+1):
            x_sub = X_train[i*batch_size:(i+1)*batch_size]
            y_sub = y_train[i*batch_size:(i+1)*batch_size]
            delta = self.alpha * self.calc_gradient(x_sub,y_sub)
            #print(delta)
            self.w -= delta
            #self.w[0]*=10

            #break
        #x_sub = X_train[i*200:(i+1)*200]
        #y_sub = y_train[i*200:(i+1)*200]
        #self.w -= self.alpha * self.calc_gradient(x_sub,y_sub)
        #print(self.w)





        return


    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Use the trained weights to predict labels for test data points.

        Parameters:
            X_test: a numpy array of shape (N, D) containing testing data;
                N examples with D dimensions

        Returns:
            predicted labels for the data in X_test; a 1-dimensional array of
                length N, where each element is an integer giving the predicted
                class.
        """

        ret = np.zeros((X_test.shape[0]))
        temp = np.zeros((X_test.shape[0],X_test.shape[1]+1)).astype(np.longdouble)
        for i in range(len(X_test)):
            temp[i] = np.append(X_test[i],1)

        dots = sum((self.w*temp).transpose())

        return np.greater(dots,0.0)
