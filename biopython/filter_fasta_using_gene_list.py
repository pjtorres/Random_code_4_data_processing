import argparse
from Bio import SeqIO

#When runnning it in jupyter notebook

# def filter_fasta(input_fasta, output_fasta, gene_list):
#     # Open the input and output FASTA files
#     with open(input_fasta, "r") as input_handle, open(output_fasta, "w") as output_handle:
#         # Iterate through the FASTA records
#         for record in SeqIO.parse(input_handle, "fasta"):
#             # Check if the record ID (assumed to be the gene ID) is in the gene list
#             if record.id in gene_list:
#                 # Write the record to the output FASTA file
#                 SeqIO.write(record, output_handle, "fasta")

# # Example usage:
# input_fasta_file = "all_genes.fa"
# output_fasta_file = "filtered_cc_genes.fa.fasta"
# gene_list =list(gene_gene_cluster['seqID'])  # Replace with your list of genes

# filter_fasta(input_fasta_file, output_fasta_file, gene_list)


# On terminal
# python script.py input.fasta output.fasta gene_list.txt

def filter_fasta(input_fasta, output_fasta, gene_list):
    # Open the input and output FASTA files
    with open(input_fasta, "r") as input_handle, open(output_fasta, "w") as output_handle:
        # Iterate through the FASTA records
        for record in SeqIO.parse(input_handle, "fasta"):
            # Check if the record ID (assumed to be the gene ID) is in the gene list
            if record.id in gene_list:
                # Write the record to the output FASTA file
                SeqIO.write(record, output_handle, "fasta")

if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Filter a FASTA file based on a list of gene IDs.")
    parser.add_argument("input_fasta", help="Input FASTA file")
    parser.add_argument("output_fasta", help="Output FASTA file")
    parser.add_argument("gene_list_file", help="File containing list of gene IDs")
    args = parser.parse_args()

    # Read gene list from file
    with open(args.gene_list_file, "r") as gene_list_handle:
        gene_list = [line.strip() for line in gene_list_handle]

    # Filter the FASTA file
    filter_fasta(args.input_fasta, args.output_fasta, gene_list)
