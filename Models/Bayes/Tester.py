import numpy as np
import Generator
import Utils

def main():
    confusionMatrix = [[0 for i in range(4)] for n in range(4)]

    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' , "X", "B", "J", "Z"]
    rng = np.random.default_rng()
    items = Utils.load()
    rng.shuffle(items)
    sco = [0,1,2,4]

    l = len(items)*2//3

    training = items[:l]
    testing = items[l:]

    (totalCounts, logCounts, wordCounts) = Generator.main(training)
    wordCounts+=len(amino_acids)**3
    print(totalCounts)
    asdf = [logCounts[n] - wordCounts[n] for n in range(len(sco))]



    for i in testing:
        expected = None
        try:
            for n in range(len(sco)):
                accumulator = wordCounts[n]
                counter = np.ones((len(amino_acids)**3))
                for j in range(len(i[1])-3):
                    ind = 0
                    for h in i[1][j:j+3]:
                        ind*=len(amino_acids)
                        ind+=amino_acids.index(h)
                    counter[ind]+=1
                accumulator+= sum((counter)*(asdf[n]))


                if expected == None:
                    expected = (accumulator,n)

                elif expected[0]<accumulator:
                    expected = (accumulator,n)
            confusionMatrix[expected[1]][sco.index(i[2])]+=1
        except:
            print(i)


    print(confusionMatrix)
    total = sum([sum(i) for i in confusionMatrix])
    rights = sum([confusionMatrix[i][i] for i in range(len(confusionMatrix))])
    print(rights/total)

if __name__ == '__main__':
    main()
