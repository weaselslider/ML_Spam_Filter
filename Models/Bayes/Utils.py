def load():
    titles = []
    sequences = []

    #load the inputs
    realProteins = ["Avinelandii.faa","Bsubtilis.faa","Ctepidum.faa","Ctrachomatis.faa","Cvibroides.faa","Dmel.faa","Dradiodurans.faa","Ecoli.faa","Fplacidus.faa","Haurantiacus.faa","Mlabreanum.faa","Mmycoides.faa","Msmithii.faa","Nviennesis.faa","Paeruginosa.faa","Rbaltica.faa","Scerevisieae.faa","Senterica.faa","Smarcecens.faa","Spneumoniea.faa","Wpipientis.faa","Zmays.faa"]

    fakeProteins = ["Reversefakeproteins_Dmel.faa","Reversefakeproteins_Ecoli.faa","fakedrosophila_proteins.faa","fakeecoli_proteins.faa","fakerandom_proteins.faa"]

    eukaryote_keywords = ['Drosophila', 'Saccharomyces', 'Zea']
    archea_keywords = ['Methanobrevibacter', 'Methanocorpusculum', 'Nitrososphaera', 'Ferroglobus']
    bacteria_keywords = ['Escherichia', 'Bacillus', 'Wolbachia', 'Sreptococcus', 'Mycoplasma', 'Serratia',
                         'Salmonella', 'Pseudomonas', 'Caulobacter', 'Aquifex', 'Deinococcus', 'Chlamydia',
                         'Rhodopirellula', 'Chlorobaculum', 'Herpetosiphon', 'Azotobacter']
    fake_keywords = ['Fake', 'Reversed']


    for i in realProteins:
        with open("../../proteomes/"+i, "r") as f:
            lines = []
            for line in f:
                if line[0] == ">":
                    if len(lines)!=0:
                        title = lines[0]
                        protein = "".join(lines[1:])
                        titles.append(title)
                        sequences.append(protein)


                    lines = []

                lines.append(line.strip())


    for i in fakeProteins:
        with open("../../proteomes/"+i, "r") as f:
            lines = []
            for line in f:
                if line[0] == ">":
                    if len(lines)!=0:
                        title = lines[0]
                        protein = "".join(lines[1:])
                        titles.append(title)
                        sequences.append(protein)


                    lines = []

                lines.append(line.strip())


    outputs = []

    for i in range(len(sequences)):
        score = None
        if   any(keyword in titles[i] for keyword in fake_keywords):score = 4
        elif any(keyword in titles[i] for keyword in eukaryote_keywords):score = 2
        elif any(keyword in titles[i] for keyword in archea_keywords):score = 1
        elif any(keyword in titles[i] for keyword in bacteria_keywords):score = 0
        if score is not None:
            outputs.append((titles[i] , sequences[i], score))
    return outputs
