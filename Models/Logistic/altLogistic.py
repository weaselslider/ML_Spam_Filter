
# importing modules
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
#import matplotlib.pyplot as plt
from tensorflow.keras import metrics

def Load():
    counter1 = 0
    out = []


    with open("../../dataset2","r") as f:
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



model = Sequential([

    # dense layer 1
    #Dense(32, activation='sigmoid'),

    # dense layer 2
    #Dense(32, activation='sigmoid'),

      # output layer
    Dense(5, activation='sigmoid'),
]) # only output layer = one layer of perceptrons. effectively same as what i was doing - testing to see differences.


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=500,
          batch_size=2000,
          validation_split=0.2)


results = model.evaluate(X_test,  Y_test, verbose = 0)
print('test loss, test acc:', results)

y_guess = model.predict(X_test)

y_altTest = np.zeros((5,len(Y_test)))
for i in range(len(y_altTest)):
    y_altTest[i] += np.equal(Y_test,i)

metric = metrics.F1Score(threshold = .5)
metric.update_state(y_altTest.transpose(),y_guess)
print("F-score",metric.result())

metric = metrics.Precision()
metric.update_state(y_altTest.transpose(),y_guess)
print("Precision",metric.result())

metric = metrics.Recall()
metric.update_state(y_altTest.transpose(),y_guess)
print("Recall",metric.result())


model.save("./LogisticModel")
