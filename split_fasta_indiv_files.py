__author__= 'Pedro J. Torres '
import os, argparse
import pandas 
from Bio import SeqIO

#--------Command line arguments -----------------------------------------
parser=argparse.ArgumentParser(description="Script willa large multi fasta file into individual files for each fasta.")
parser.add_argument('-i','--input', help='Input fasta file',required=True)

args = parser.parse_args()
inputfile=str(args.input)

fasta_sequence = SeqIO.parse(open(inputfile),'fasta')
for fasta in fasta_sequence:
    
    name, sequence = fasta.id, str(fasta.seq)
    fout = open(name+".fna",'w')
    fout.write(">"+name+'\n'+sequence)
    fout.close()
    
