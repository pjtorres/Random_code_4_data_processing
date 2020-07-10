__author__= 'Pedro J. Torres'
import argparse
import os
from Bio import Entrez
from Bio import SeqIO

#-----------Command Line Arguments-----------------
parser=argparse.ArgumentParser(description="This script uses python3 and Biopython. Make sure both are installed. Script will take a list of taxa, get an accesion number associated with it and then use that to return the taxa lineage.")
parser.add_argument('-i','--input', help=' Input list of taxa for which you wish to pull taxonomic lineage information.',required=True)
parser.add_argument('-o','--output',help='Output file with taxa name and lineage associated with it.', required=False)

args = parser.parse_args()
inputfile=str(args.input) #name of fasta file want to change
outputfile=str(args.output) # name of output file with new header


# give email to Entrez, pseudo below works fine too
Entrez.email = "Your.Name.Here@example.org"

#make new file and open incoming file
fout = open(outputfile, 'w+')
fin = open(inputfile, 'r')

fout.write('taxa'+'\t'+'taxonomic_lineage'+'\n')
for line in fin:
    line = line.strip()
    print(line)
    taxa = str(line+'[ORGN]')
    
    #start by getting an accesion number that is associated with a genome beloging to this particular taxa
    handle = Entrez.esearch(db="nucleotide", retmax=10, term=taxa, idtype="acc")
    records = Entrez.read(handle)
    accesion = records.get('IdList')[0]

    #now that we have the accesion, we can get the taxonomic lineage associated with it
    handle = Entrez.efetch(db="nucleotide", id=str(accesion), rettype="gb", retmode="text")
    x = SeqIO.read(handle, 'genbank')# get information regarding your accesion number in here will be taxonomy
    tax=x.annotations['taxonomy']# only get taxonomy

    taxf=";".join(tax)#join taxonomy based on ';' character
    full_lineage=(taxf+';'+x.annotations['organism']) # but i also want the organism name so this will also add organism specific name
    fout.write(line+'\t'+full_lineage+'\n')
    
fout.close()
fin.close()
print('Done! :)')
