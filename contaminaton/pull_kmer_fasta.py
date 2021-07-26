__author__= 'Pedro J. Torres'
import pandas
from Bio import SeqIO
import matplotlib.pyplot as plt
import os, argparse


#python get_fasta_kmer.py --fna FN668691.1.fna  -s 3733 -e 3999 -o FN668691.1.contamination

'''
Script will allow you to generate pull out a nucleotides in a fasta file from a single particular region
'''




#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script will allow you to generate a pair of socs based on genome coverage output from bedtools genomecoverage.")
parser.add_argument('-fna','--fna', help='Fasta file containing signatures of desired SOCS. ', required=True)
parser.add_argument('-o','--output', help='Name of taxa for which you are generating new SOCS.', required=True)
parser.add_argument('-s','--start', help='Regional start site of probe.', required=True)
parser.add_argument('-e','--end', help='Regional end site of probe.', required=True)


#Pass arguments
args = parser.parse_args()
fna=args.fna
output = str(args.output)
instart=int(args.start)
inend=int(args.end)

# generate diurectories
cwd = os.getcwd()+'/'


# start parsing your genome coverage file -----------------

fin = open(fna, 'r')
out=open(output,'w+')
fasta_sequences = SeqIO.parse(open(fna),'fasta')
for fasta in fasta_sequences:
    name, sequence = fasta.id, str(fasta.seq)
    SOC = sequence[instart:inend]
    out.write(">"+ name +'_'+str(instart)+'_'+str(inend)+ '\n'+SOC+'\n')


out.close()

#os.rename(old, new)


print('Done!')
