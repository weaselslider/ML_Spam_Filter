import os
import glob
from collections import Counter
import itertools
import re

class ProteinAttributeParser:
    def __init__(self, output_filename="combined_proteins.txt"):
        self.output_filename = output_filename

    def combine_files(self):
        # Collect all files with .fasta extension in the current directory
        fasta_files = glob.glob('*.faa')

        with open(self.output_filename, 'w') as output_file:
            for fasta_file in fasta_files:
                with open(fasta_file, 'r') as f:
                    sequence_name = ''
                    sequence = ''
                    for line in f:
                        line = line.strip()  # Remove any newline characters
                        if not line:
                            continue  # Skip empty lines
                        if line.startswith('>'):
                            # If we already have a sequence name before, write the previous sequence to the output
                            if sequence_name:
                                output_file.write(f"{sequence_name},{sequence}\n")
                                sequence = ''  # Reset sequence for the next protein
                            sequence_name = line[1:]  # Remove the ">" character
                        else:
                            sequence += line

                    # Write the last sequence in the file, if any
                    if sequence_name:
                        output_file.write(f"{sequence_name},{sequence}\n")

    def find_common_subwords(self, input_filename, subword_sizes=[2, 3], top_n=10):
        subword_counters = {size: Counter() for size in subword_sizes}
        sequence_count = 0

        with open(input_filename, 'r') as file:
            for line in file:
                name, sequence = line.strip().split(',', 1)
                for size in subword_sizes:
                    for i in range(0, len(sequence) - size + 1):
                        subword = sequence[i:i+size]
                        subword_counters[size][subword] += 1

                sequence_count += 1
                if sequence_count % 1000 == 0:
                    print(f"Processed {sequence_count} sequences...")

        for size, counter in subword_counters.items():
            print(f"\nTop {top_n} most common {size}-amino acid subwords:")
            for subword, count in counter.most_common(top_n):
                print(f"{subword}: {count} occurrences")

    def find_least_common_subwords(self, input_filename, subword_sizes=[2, 3], top_n=10):
        # Define the 20 common amino acids
        amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
        # Generate all possible subwords of the given sizes
        all_subwords = {size: [''.join(comb) for comb in itertools.product(amino_acids, repeat=size)] for size in subword_sizes}
    
        # Initialize the counters with 0 for each subword
        subword_counters = {size: Counter({subword: 0 for subword in all_subwords[size]}) for size in subword_sizes}
    
        sequence_count = 0

        with open(input_filename, 'r') as file:
            for line in file:
                _, sequence = line.strip().split(',', 1)
                for size in subword_sizes:
                    for i in range(0, len(sequence) - size + 1):
                        subword = sequence[i:i+size]
                        if subword in subword_counters[size]:  # Only update counts for valid amino acid combinations
                            subword_counters[size][subword] += 1

                sequence_count += 1
                if sequence_count % 1000 == 0:
                    print(f"Processed {sequence_count} sequences...")

        for size, counter in subword_counters.items():
            print(f"\nTop {top_n} least common {size}-amino acid subwords:")
            for subword, count in counter.most_common()[:-top_n-1:-1]:  # This extracts the least common elements
                print(f"{subword}: {count} occurrences")

    def calculate_molecular_mass(self, input_filename, output_filename):
            # Define the molecular weights for the 20 common amino acids in Daltons (Da)
            amino_acids_weights = {
                'A': 71.08, 'C': 103.15, 'D': 115.09, 'E': 129.12,
                'F': 147.18, 'G': 57.05, 'H': 137.14, 'I': 113.16,
                'K': 128.18, 'L': 113.16, 'M': 131.20, 'N': 114.11,
                'P': 97.12, 'Q': 128.14, 'R': 156.19, 'S': 87.08,
                'T': 101.11, 'V': 99.13, 'W': 186.21, 'Y': 163.18
            }

            with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
                for line in infile:
                    name, sequence = line.strip().split(',', 1)
                    molecular_mass = sum(amino_acids_weights.get(aa, 0) for aa in sequence)  # Calculate total weight with a default value of 0 if aa isn't recognized
                    molecular_mass_kDa = molecular_mass / 1000  # Convert to kiloDaltons (kDa)
                
                    outfile.write(f"{name},{sequence},{molecular_mass_kDa:.2f}\n")
                    
    def remove_commas_before_first_bracket(self, input_filename, output_filename):
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                # Find the position of the first ']' character
                pos = line.find(']')
                if pos != -1:  # Only proceed if there's a ']' in the line
                    # Remove all commas before the position of the first ']'
                    modified_start = line[:pos].replace(',', '')
                    line = modified_start + line[pos:]
                outfile.write(line)
                
    def append_sequence_length(self, input_filename, output_filename):
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                if len(data) < 2:  # Ensure there's at least an identifier and a sequence
                    continue
                sequence = data[1]
                sequence_length = len(sequence)
                
                # Append sequence length to the data and write to the output file
                data.append(str(sequence_length))
                outfile.write(f"{','.join(data)}\n")
    
    def append_protein_charge(self, input_filename, output_filename):
        # Define average pKa values for ionizable groups in amino acids
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

        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                if len(data) < 2:
                    continue
                sequence = data[1]
                charge = 0.0

                # Calculate the charge contributed by each amino acid and terminus
                for aa, pka in pka_values.items():
                    if aa == 'N_term':
                        charge += 1 / (1 + 10**(pH - pka)) # Positive charge
                    elif aa == 'C_term':
                        charge -= 1 / (1 + 10**(pka - pH)) # Negative charge
                    else:
                        charge += sequence.count(aa) * (1 / (1 + 10**(pH - pka)) if aa in "HRKY" else -1 / (1 + 10**(pka - pH)))

                # Append the charge to the data and write to the output file
                data.append(str(charge))
                outfile.write(f"{','.join(data)}\n")
                
    def calculate_charge(self, sequence, pH, pka_values):
        charge = 0.0

        # Calculate the charge contributed by each amino acid and terminus
        for aa, pka in pka_values.items():
            if aa == 'N_term':
                charge += 1 / (1 + 10**(pH - pka))  # Positive charge
            elif aa == 'C_term':
                charge -= 1 / (1 + 10**(pka - pH))  # Negative charge
            else:
                charge += sequence.count(aa) * (1 / (1 + 10**(pH - pka)) if aa in "HRKY" else -1 / (1 + 10**(pka - pH)))
        return charge

    def find_pI(self, sequence, pka_values):
        low_pH = 0
        high_pH = 14
        tolerance = 0.0001
        max_iterations = 1000
        iteration = 0
    
        while iteration < max_iterations:
            mid_pH = (low_pH + high_pH) / 2
            charge = self.calculate_charge(sequence, mid_pH, pka_values)

            if abs(charge) < tolerance:
                return mid_pH
            elif charge > 0:
                low_pH = mid_pH
            else:
                high_pH = mid_pH
        
            iteration += 1

        return mid_pH

    def calculate_and_append_pI(self, input_filename, output_filename, pka_values):
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                sequence = data[1]
                pI = self.find_pI(sequence, pka_values)
            
                # Append the pI to the data and write to the output file
                data.append(str(pI))
                outfile.write(f"{','.join(data)}\n")
                
    def calculate_gravy(self, input_file, output_file):
        # Define Kyte & Doolittle hydropathy values
        kd_values = {
            'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5, 'M': 1.9, 'A': 1.8, 
            'G': -0.4, 'T': -0.7, 'S': -0.8, 'W': -0.9, 'Y': -1.3, 'P': -1.6, 
            'H': -3.2, 'E': -3.5, 'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
        }
    
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                sequence = data[1]
                gravy = sum([kd_values[aa] for aa in sequence if aa in kd_values]) / len(sequence)
            
                # Append the gravy score to the data and write to the output file
                data.append(str(gravy))
                outfile.write(','.join(data) + '\n')

    def calculate_aa_percentage(self, input_file, output_file):
        """
        Calculate the percentage of each amino acid in protein sequences from the input_file
        and write the results in the output_file.

        For each protein:
        The percentages will be written in the order of the following amino acids:
        A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y
        """

        # List of amino acids in the order they'll be processed
        amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                protein_sequence = data[1]
                protein_length = len(protein_sequence)

                # Calculate percentage for each amino acid
                percentages = []
                for aa in amino_acids:
                    percentage = (protein_sequence.count(aa) / protein_length) * 100
                    rounded_percentage = round(percentage, 1)
                    percentages.append(str(rounded_percentage))

                # Write the original data followed by the calculated percentages to the output file
                outfile.write(','.join(data + percentages) + '\n')

    def check_subwords(self, input_file, output_file):
        """
        Determine if each protein sequence in the input_file contains the specified subwords.
    
        For each protein:
        The presence (1) or absence (0) of each subword will be written in the order of:
        AA, LA, AL, GG, MC, CM, LAA, AAL, LLA, PPA
        """

        # List of subwords in the order they'll be checked
        subwords = ["AA", "LA", "AL", "GG", "MC", "CM", "LAA", "AAL", "LLA", "PPA"]

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                protein_sequence = data[1]

                # Check presence of each subword in the protein sequence
                scores = []
                for subword in subwords:
                    score = 1 if subword in protein_sequence else 0
                    scores.append(str(score))

                # Write the original data followed by the subword presence scores to the output file
                outfile.write(','.join(data + scores) + '\n')

    def categorize_proteins(self, input_file, output_file):
        """
        Categorize each protein based on the presence of specific subwords in its name:
    
        2: eukaryote derived
        1: archea derived
        0: bacteria derived
        4: fake protein
    
        If the name contains 'Drosophila', 'Saccharomyces', or 'Zea', it's categorized as eukaryote derived.
        If the name contains 'Methanobrevibacter', 'Methanocorpusculum', 'Nitrososphaera', or 'Ferroglobus', 
        it's categorized as archea derived.
        If the name contains any of ['Escherichia', 'Bacillus', ...], it's categorized as bacteria derived.
        If the name contains 'Fake' or 'Reversed', it's categorized as fake protein.
        """

        eukaryote_keywords = ['Drosophila', 'Saccharomyces', 'Zea']
        archea_keywords = ['Methanobrevibacter', 'Methanocorpusculum', 'Nitrososphaera', 'Ferroglobus']
        bacteria_keywords = ['Escherichia', 'Bacillus', 'Wolbachia', 'Sreptococcus', 'Mycoplasma', 'Serratia',
                             'Salmonella', 'Pseudomonas', 'Caulobacter', 'Aquifex', 'Deinococcus', 'Chlamydia',
                             'Rhodopirellula', 'Chlorobaculum', 'Herpetosiphon', 'Azotobacter']
        fake_keywords = ['Fake', 'Reversed']

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                data = line.strip().split(',')
                protein_name = data[0]

                score = None
                if any(keyword in protein_name for keyword in fake_keywords):
                    score = 4
                elif any(keyword in protein_name for keyword in eukaryote_keywords):
                    score = 2
                elif any(keyword in protein_name for keyword in archea_keywords):
                    score = 1
                elif any(keyword in protein_name for keyword in bacteria_keywords):
                    score = 0

                # If score is assigned, append to the data
                if score is not None:
                    outfile.write(','.join(data + [str(score)]) + '\n')
                else:
                    outfile.write(','.join(data) + '\n')  # Write original data if no category matched

if __name__ == "__main__":
    #usage
    combiner = ProteinAttributeParser()
    # Assuming 'input_filename.txt' as the specific input file you want to analyze.
    #combiner.find_common_subwords('TestProteins.txt')
    #combiner.find_least_common_subwords('FakeProteins.txt')
    #combiner.calculate_molecular_mass('TestProteins.txt', 'output_with_masses.txt')
    #combiner.remove_commas_before_first_bracket('FakeProteins.txt', 'output_without_commas.txt')
    #combiner.append_sequence_length('FakeProteins.txt', 'output_with_appended_lengths.txt')
    #combiner.append_protein_charge('FakeProteins.txt', 'output_with_appended_pi.txt')
    #pka_values = {
    #    'C': 8.5,  # Cysteine
    #    'D': 3.9,  # Aspartic acid
    #    'E': 4.3,  # Glutamic acid
    #    'H': 6.0,  # Histidine
    #    'K': 10.5,  # Lysine
    #    'R': 12.5,  # Arginine
    #    'Y': 10.1,  # Tyrosine
    #    'N_term': 8.0,  # N-terminus
    #    'C_term': 3.1   # C-terminus
    #}
    #combiner.calculate_and_append_pI('FakeProteins.txt', 'output_with_appended_pi.txt', pka_values)
    #combiner.calculate_gravy('FakeProteins.txt', 'output_gravy.txt')
    #combiner.calculate_aa_percentage('FakeProteins.txt', 'output_with_percentages.txt')
    #combiner.check_subwords('FakeProteins.txt', 'output_with_subword_scores.txt')
    combiner.categorize_proteins('FakeProteins.txt', 'categorized_output.txt')

#if __name__ == "__main__":
#    combiner = ProteinAttributeParser()
#    combiner.combine_files()
#    print(f"Proteins combined and saved to {combiner.output_filename}.")
