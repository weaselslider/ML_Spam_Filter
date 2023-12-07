import numpy as np


def Load():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    titles = []
    inputs = []

    #load the inputs
    realProteins = ["Avinelandii.faa","Bsubtilis.faa","Ctepidum.faa","Ctrachomatis.faa","Cvibroides.faa","Dmel.faa","Dradiodurans.faa","Ecoli.faa","Fplacidus.faa","Haurantiacus.faa","Mlabreanum.faa","Mmycoides.faa","Msmithii.faa","Nviennesis.faa","Paeruginosa.faa","Rbaltica.faa","Scerevisieae.faa","Senterica.faa","Smarcecens.faa","Spneumoniea.faa","Wpipientis.faa","Zmays.faa"]

    fakeProteins = ["Reversefakeproteins_Dmel.faa","Reversefakeproteins_Ecoli.faa","fakedrosophila_proteins.faa","fakeecoli_proteins.faa","fakerandom_proteins.faa"]


    for i in realProteins:
        with open("./proteomes/"+i, "r") as f:
            lines = []
            for line in f:
                if line[0] == ">":
                    if len(lines)!=0:
                        title = lines[0]
                        protein = "".join(lines[1:])
                        titles.append(title)
                        inputs.append(protein)


                    lines = []

                lines.append(line.strip())


    for i in fakeProteins:
        with open("./proteomes/"+i, "r") as f:
            lines = []
            for line in f:
                if line[0] == ">":
                    if len(lines)!=0:
                        title = lines[0]
                        protein = "".join(lines[1:])
                        titles.append(title)
                        inputs.append(protein)


                    lines = []

                lines.append(line.strip())






    #output = []
    #outputLabels = np.zeros((len(inputs)))
    #outputLabels+=labels
    #make the np arrays
    #for i in range(2): # 2 seems like it'll be fine. 3 throws me an error, and says it requires 32.8 GiB for the set.
        #item = np.zeros((len(inputs),len(alphabet)**(i+1)))


        #loadIntoArray(inputs,item, i+1)

        #output.append( item ) #zeros array to put lengths in, and labels.


    #return (output, inputs, labels)
    #loop to add the datum in.

    return (titles,inputs)




    #performance improvement ideas: just use 32 instead of alphabet length. then bitshift instead of multiply. slightly less space efficient, but eh.


def GetSubstrs(inputs, lengths):
    output = []
    for i in range(len(inputs)-lengths+1) :
        output.append(inputs[i:i+lengths])
    return output


def loadIntoArray(inputs, outputs, length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(inputs)):
        index = 0
        for n in GetSubstrs(inputs[i],length):
            for z in n:
                index*=len(alphabet)
                try:
                    index+=alphabet.index(z)
                except:
                    raise Exception("Failed to find a letter in alphabet:"+str([z])+" "+str(n)+" "+inputs[i])
