
import random
print("test")
class ProteinGenerator:
    def __init__(self, num_proteins):
        self.num_proteins = num_proteins
        self.amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        
        # Simplified E.coli amino acid frequencies (these are percentages from Genscript)
        self.ecoli_amino_freq = {
            'A': 0.010, 'C': 0.012, 'D': 0.056, 'E': 0.062, 'F': 0.041,
            'G': 0.079, 'H': 0.023, 'I': 0.065, 'K': 0.051, 'L': 0.110,
            'M': 0.028, 'N': 0.045, 'P': 0.045, 'Q': 0.046, 'R': 0.059,
            'S': 0.066, 'T': 0.059, 'V': 0.075, 'W': 0.015, 'Y': 0.032
        }

        # Hypothetical Drosophila amino acid frequencies (these are percentages from Genscript)
        self.drosophila_amino_freq = {
            'A': 0.110, 'C': 0.027, 'D': 0.076, 'E': 0.093, 'F': 0.051,
            'G': 0.091, 'H': 0.039, 'I': 0.071, 'K': 0.082, 'L': 0.132,
            'M': 0.034, 'N': 0.069, 'P': 0.080, 'Q': 0.077, 'R': 0.081,
            'S': 0.122, 'T': 0.082, 'V': 0.087, 'W': 0.014, 'Y': 0.043
        }

    def generate_random_proteins(self, output_file):
        with open(output_file, 'w') as f:
            for i in range(self.num_proteins):
                length = random.randint(49, 999)  # Adjusted for the added Methionine
                protein = 'M' + ''.join(random.choice(self.amino_acids) for _ in range(length))
                f.write(f">FakeRandomProtein_{i+1}\n")
                f.write(protein + "\n")
                
    def generate_ecoli_preference_proteins(self, output_file):
        with open(output_file, 'w') as f:
            for i in range(self.num_proteins):
                length = random.randint(49, 999)
                protein = 'M' + ''.join(random.choices(self.amino_acids, weights=self.ecoli_amino_freq.values(), k=length))
                f.write(f">FakeEcoliProtein_{i+1}\n")
                f.write(protein + "\n")

    def generate_drosophila_preference_proteins(self, output_file):
        with open(output_file, 'w') as f:
            for i in range(self.num_proteins):
                length = random.randint(49, 999)
                protein = 'M' + ''.join(random.choices(self.amino_acids, weights=self.drosophila_amino_freq.values(), k=length))
                f.write(f">FakeDrosophilaProtein_{i+1}\n")
                f.write(protein + "\n")

    def reverse_random_proteins_to_fasta(self, fasta_file):
        """
        Takes a FASTA file of proteins, selects 10 proteins at random, 
        and writes their reversed sequences with a Methionine "M" prefix
        to a new FASTA file, with headers prefixed by "Reversed".

        Args:
        - fasta_file (str): Path to the FASTA file
        """
        headers = []
        proteins = []

        with open(fasta_file, 'r') as file:
            header = None
            sequence = ""
            for line in file:
                line = line.strip()
                if line.startswith(">"):
                    if header:
                        headers.append(header)
                        proteins.append(sequence)
                    header = line
                    sequence = ""
                else:
                    sequence += line
            if header and sequence:  # For the last sequence in the file
                headers.append(header)
                proteins.append(sequence)

        # Zip headers and proteins for random sampling
        fasta_entries = list(zip(headers, proteins))
        selected_entries = random.sample(fasta_entries, 4000) if len(fasta_entries) > 10 else fasta_entries

        # Write reversed sequences with "M" prefix to new fasta file
        with open("reversefakeproteins.fasta", 'w') as output_file:
            for header, protein in selected_entries:
                reversed_protein = "M" + protein[::-1]
                reversed_header = ">Reversed" + header[1:]
                output_file.write(reversed_header + '\n')
                output_file.write(reversed_protein + '\n')



# Usage:
#print("starting to generate proteins")
#protein_gen = ProteinGenerator(num_proteins=25000)
#protein_gen.generate_random_proteins("random_proteins.fasta")
#protein_gen.generate_ecoli_preference_proteins("ecoli_proteins.fasta")
#protein_gen.generate_drosophila_preference_proteins("drosophila_proteins.fasta")
#print("done generating proteins")

# Usage
print("reversing some proteins")
protein_gen = ProteinGenerator(num_proteins=25000)
fasta_file_path = "Bsubtilis.faa"
protein_gen.reverse_random_proteins_to_fasta(fasta_file_path)
print("done reversing some proteins")