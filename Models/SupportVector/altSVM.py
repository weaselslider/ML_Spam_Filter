
#import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import numpy as np



def Load():
    counter1 = 0
    out = []


    with open("../../dataset","r") as f:
        for l in f:
            item = l.strip().split("\t")
            if(len(item[2:])!=36):
                print(item)
            else:
                out.append(item)



    output = np.zeros((len(out),len(out[0][2:]))).astype(np.longdouble)


    for i in range(len(out)):
        try:
            sli = [float(i) for i in out[i][2:]]
            output[i]+=sli
        except:
            print("Confusion:", out[i])

    np.random.default_rng().shuffle(output)

    partition = int(len(output)*2/3)

    train = output[0:partition]
    testing = output[partition:]



    X_train = train[:,:-1]
    Y_train = train[:,-1]

    X_test = testing[:,:-1]
    Y_test = testing[:,-1]

    #print(output.shape)
    #print(X_train.shape)
    #print(Y_train.shape)
    #print(X_test.shape)
    #print(Y_test.shape)



    return (X_train,Y_train,X_test,Y_test)

(X_train,Y_train,X_test,Y_test) = Load()


svm = SVC(kernel="rbf", gamma=0.5, C=.75)

svm.fit(X_train, Y_train)

y_guess = svm.predict(X_test)

print(classification_report(Y_test,y_guess))
