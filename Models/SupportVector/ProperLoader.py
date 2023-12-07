import numpy as np
import svm
import json

def test(X_test,Y_test,models):
    labels = [0,1,2,4]
    outs = []
    for i in range(len(models)):
        outs.append([])
        for n in range(len(models)):
            outs[-1].append(0)
    ps = [pred(X_test,model.w) for model in models]
    counter=0
    for i in range(len(X_test)):
        actual = labels.index(Y_test[i])
        max = ps[3][i]
        expected = 3
        for n in range(len(models)):
            counter+=1
            if ps[n][i]>max:
                max = ps[n][i]
                Expected = n
        outs[expected][actual] +=1

    print(outs,end=" ")
    print(sum([outs[i][i] for i in range(4)]),end = "  ")
    
    print("Just Fake: ",end = " ")
    ys = np.equal(Y_test, 4.0)
    t = models[-1].predict(X_test)
    acts = [[0,0],[0,0]]
    for i in range(len(X_test)):
        acts[int(ys[i])][int(t[i])]+=1
    print(acts,end = " ")
    print((acts[0][0]+acts[1][1])/len(X_test),end="")
    print("  ",end="")



    return outs

def pred(X_test,w):
    ret = np.zeros((X_test.shape[0]))
    temp = np.zeros((X_test.shape[0],X_test.shape[1]+1)).astype(np.longdouble)
    for i in range(len(X_test)):
        temp[i] = np.append(X_test[i],1)
    dots = sum((w*temp).transpose())
    ps = np.zeros(X_test.shape[0])
    for i in range(len(ps)):
        ps[i] = 1/(1+np.exp(-dots[i])) if dots[i]>0 else np.exp(dots[i])/(1+np.exp(dots[i]))
    return dots

def train(X_train,Y_train):
    labels = [0,1,2,4]
    models = []

    for i in labels:
        y_temp = np.equal(Y_train, i).astype(np.longdouble)
        model = svm.SVM(len(X_train[0]),.4,100,.1)
        model.train(X_train,y_temp)
        models.append(model)
    return models


def trainOne(X_train,Y_train,models):
    labels = [0,1,2,4]
    for i in range(len(labels)):
        y_temp = np.equal(Y_train, labels[i]).astype(np.longdouble)
        models[i].train_one(X_train,y_temp)
    return models

def doTheThing(items):
    (X_train,Y_train,X_test,Y_test) = items
    models = train(X_train,Y_train)
    print(([model.w for model in models]))
    for i in range(1000):
        trainOne(X_train,Y_train,models)
        print(i,calcAccuracy(test(X_test,Y_test,models)),calcAccuracy(test(X_train,Y_train,models)),end="")
        print("Just Fake: ",end = " ")
        ys = np.equal(Y_test, 4.0)
        t = models[-1].predict(X_test)
        acts = [[0,0],[0,0]]
        for i in range(len(X_test)):
            acts[int(ys[i])][int(t[i])]+=1
        print(acts,end = " ")
        print((acts[0][0]+acts[1][1])/len(X_test))
    print(([model.w for model in models]))


def calcAccuracy(confusionMatrix):
    total = sum([sum(i) for i in confusionMatrix])
    rights = sum([confusionMatrix[i][i] for i in range(len(confusionMatrix))])
    return rights/total









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


if __name__ == '__main__':
    doTheThing(Load())
