"""Logistic regression model."""

import numpy as np
import warnings
warnings.filterwarnings('error')


class Logistic:
    def __init__(self, lr: float, epochs: int):
        """Initialize a new classifier.

        Parameters:
            lr: the learning rate
            epochs: the number of epochs to train for
        """
        self.w = None  # TODO: change this #not changing this.
        self.lr = lr
        self.epochs = epochs
        self.threshold = 0.5

    def sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid function.

        Parameters:
            z: the input

        Returns:
            the sigmoid of the input
        """

        return np.exp(z)/(1+np.exp(z))

    def train_one(self, X_train: np.ndarray, y_train: np.ndarray):
        temp = np.zeros((X_train.shape[0],X_train.shape[1]+1)).astype(np.longdouble)
        for i in range(len(X_train)):
            temp[i] = np.append(X_train[i],1)
        dots = sum(( temp * self.w).transpose())

        #zs = np.exp(dots)
        #ps = zs / (1+zs)
        #^ np.exp will occasionally give overflow errors. so,
        ps = np.zeros(y_train.shape)
        for i in range(len(ps)):
            ps[i] = 1/(1+np.exp(-dots[i])) if dots[i]>0 else np.exp(dots[i])/(1+np.exp(dots[i]))
        ds = y_train - ps
        w_diff = np.zeros(temp.shape).astype(np.longdouble)
        for i in range(len(w_diff)):
            w_diff[i]+= ds[i] * temp[i]
        w_delta = sum(w_diff)
        self.w+= self.lr * w_delta



    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the classifier.

        Use the logistic regression update rule as introduced in lecture.

        Parameters:
            X_train: a numpy array of shape (N, D) containing training data;
                N examples with D dimensions
            y_train: a numpy array of shape (N,) containing training labels
        """
        


        self.w = np.zeros((len(X_train[0])+1)).astype(np.longdouble)

        temp = np.zeros((X_train.shape[0],X_train.shape[1]+1)).astype(np.longdouble) # yes i'm aware this could be optimized by
        for i in range(len(X_train)):
            temp[i] = np.append(X_train[i],1)

        for i in range(self.epochs):

            try:


                dots = sum(( temp * self.w).transpose())

                #zs = np.exp(dots)
                #ps = zs / (1+zs)
                #^ np.exp will occasionally give overflow errors. so,
                ps = np.zeros(y_train.shape)
                for i in range(len(ps)):
                    ps[i] = 1/(1+np.exp(-dots[i])) if dots[i]>0 else np.exp(dots[i])/(1+np.exp(dots[i]))
                ds = y_train - ps
                w_diff = np.zeros(temp.shape).astype(np.longdouble)
                for i in range(len(w_diff)):
                    w_diff[i]+= ds[i] * temp[i]
                w_delta = sum(w_diff)
                #print(w_delta.shape)
                #break
                #print(w_delta)


                self.w+= self.lr * w_delta
                #print(self.w)
                #print("<><")
            except OverflowError as e:
                print(e)
                break

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

        ps = np.zeros(X_test.shape[0])
        for i in range(len(ps)):
            ps[i] = 1/(1+np.exp(-dots[i])) if dots[i]>0 else np.exp(dots[i])/(1+np.exp(dots[i]))
        return np.greater(ps,.5)
