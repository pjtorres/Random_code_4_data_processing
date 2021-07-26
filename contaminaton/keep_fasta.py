__author__= 'Pedro J. Torres'
import pandas
from Bio import SeqIO

import os, argparse



'''
python keep_fasta.py -fna ticket_subset/GCA_000338855.1_EHA_ku27_v1_genomic.fna -o KB444062.1.fna -k KB444062.1
'''




#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script will allow you to generate a pair of socs based on genome coverage output from bedtools genomecoverage.")
parser.add_argument('-fna','--fna', help='Fasta file containing signatures of desired contigs. ', required=True)
parser.add_argument('-o','--output', help='Name of taxa for which you are generating new SOCS.', required=True)
parser.add_argument('-k','--keep', help='Contig or gene you wish to keep.', required=True)



#Pass arguments
args = parser.parse_args()
fna=args.fna
out = str(args.output)
keep=str(args.keep)


input=fna

# input='GCA_006942135.1_ASM694213v1_genomic.fna'
# keep='PQTP01000029.1'
# out='tmp_GCA_006942135.1_ASM694213v1_genomic.fna'

wanted = (rec for rec in SeqIO.parse(input, "fasta") \
                        if rec.id.startswith(keep))
count = SeqIO.write(wanted, out, "fasta")
print ("Saved %i records" % count)

# keep a particular fasta in a multi fasta file beased on heaeder
