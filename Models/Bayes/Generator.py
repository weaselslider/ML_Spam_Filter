import numpy as np
import Utils


def main(items):
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' , "X", "B", "J", "Z"]
    #X,B,J, Z are not amino acids, but stand in for a subset (or any in the case of X) https://en.wikipedia.org/wiki/FASTA_format#Sequence_representation
    #a probably good idea is to expand them into all possible proteins from those substitutions. but for now...
    sco = [0,1,2,4]

    outputs = []
    for i in range(4):outputs.append(np.ones((len(amino_acids)**3)))
    counts = [0 for _ in range(4)]
    words = [0 for _ in range(4)]



    for i in range(len(items)):
        index = sco.index(items[i][2])
        counts[index]+=1
        try:
            for n in range(len(items[i][1])-3):
                ind = 0
                for j in items[i][1][n:n+3]:
                    ind*=len(amino_acids)
                    ind+=amino_acids.index(j)
                outputs[index][ind]+=1
                words[index]+=1
                #i think, theoretically, that aligning it to 32 instead of 20 (24) could be more efficient, but should work fine.
        except:
            print(items[i][0])


    return (counts, np.log(outputs), np.log(words))

if __name__ == '__main__':
    main(Utils.load())
