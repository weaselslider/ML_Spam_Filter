import numpy as np
import loader
from ProteinAttributeParser import ProteinAttributeParser

'''
makes dataset (.tsv)
'''





def Load():
    (titles,sequences) = loader.Load()

    parser = ProteinAttributeParser()


    #here be constants.
    amino_acids_weights = {
        'A': 71.08, 'C': 103.15, 'D': 115.09, 'E': 129.12,
        'F': 147.18, 'G': 57.05, 'H': 137.14, 'I': 113.16,
        'K': 128.18, 'L': 113.16, 'M': 131.20, 'N': 114.11,
        'P': 97.12, 'Q': 128.14, 'R': 156.19, 'S': 87.08,
        'T': 101.11, 'V': 99.13, 'W': 186.21, 'Y': 163.18
    }

    pka_values = {
        'C': 8.5,  # Cysteine
        'D': 3.9,  # Aspartic acid
        'E': 4.3,  # Glutamic acid
        'H': 6.0,  # Histidine
        'K': 10.5, # Lysine
        'R': 12.5, # Arginine
        'Y': 10.1, # Tyrosine
        'N_term': 8.0, # N-terminus
        'C_term': 3.1  # C-terminus
    }
    pH = 7.0

    subwords = ["AA", "LA", "AL", "GG", "MC", "CM", "LAA", "AAL", "LLA", "PPA"]

    kd_values = {
        'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5, 'M': 1.9, 'A': 1.8,
        'G': -0.4, 'T': -0.7, 'S': -0.8, 'W': -0.9, 'Y': -1.3, 'P': -1.6,
        'H': -3.2, 'E': -3.5, 'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
    }

    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    subwords = ["AA", "LA", "AL", "GG", "MC", "CM", "LAA", "AAL", "LLA", "PPA"]

    eukaryote_keywords = ['Drosophila', 'Saccharomyces', 'Zea']
    archea_keywords = ['Methanobrevibacter', 'Methanocorpusculum', 'Nitrososphaera', 'Ferroglobus']
    bacteria_keywords = ['Escherichia', 'Bacillus', 'Wolbachia', 'Sreptococcus', 'Mycoplasma', 'Serratia',
                         'Salmonella', 'Pseudomonas', 'Caulobacter', 'Aquifex', 'Deinococcus', 'Chlamydia',
                         'Rhodopirellula', 'Chlorobaculum', 'Herpetosiphon', 'Azotobacter']
    fake_keywords = ['Fake']#, 'Reversed']





    #params = np.zeros( (titles , 36) ) ) #i would use this if i was returning, but i'm just formatting and writing out.
    out = []
    errors = []


    for i in range(len(titles)):

        molecular_mass = sum(amino_acids_weights.get(aa, 0) for aa in sequences[i])
        molecular_mass_kDa = molecular_mass / 1000


        sequence_length = len(sequences[i])

        charge = parser.calculate_charge(sequences[i],pH,pka_values)

        pI = parser.find_pI(sequences[i],pka_values)

        gravy = sum([kd_values[aa] for aa in sequences[i] if aa in kd_values]) / len(sequences[i])

        percentages = []
        for aa in amino_acids:
            percentage = (sequences[i].count(aa) / sequence_length) * 100
            rounded_percentage = round(percentage, 1)
            percentages.append(str(rounded_percentage))

        scores = []
        for subword in subwords:
            score = 1 if subword in sequences[i] else 0
            scores.append(str(score))

        score = None
        if any(keyword in titles[i] for keyword in fake_keywords):score = 4
        elif any(keyword in titles[i] for keyword in eukaryote_keywords):score = 2
        elif any(keyword in titles[i] for keyword in archea_keywords):score = 1
        elif any(keyword in titles[i] for keyword in bacteria_keywords):score = 0

        asdf = [titles[i],sequences[i],f"{molecular_mass_kDa:.2f}",str(sequence_length),f"{charge:.2f}",f"{pI:.2f}",f"{gravy:.2f}"]+percentages+scores
        if score is not None:
            out.append("\t".join(asdf+[str(score)]))
        else:
            print(titles[i])
            errors.append("\t".join(asdf))

    with open("dataset2","w") as f:
        f.write("\n".join(out))
    with open("errors2","w") as f:
        f.write("\n".join(errors))

if __name__ == '__main__':
    Load()
