__author__= 'Pedro J. Torres - 2019 '
import subprocess
from Bio import SeqIO
import os,argparse
from Bio import Entrez
import re
import pandas, numpy
import urllib, urllib2

# pip install biopython
#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script allows you to count the number of raw reads in a given fastq.gz file ")
parser.add_argument('-i','--input', help='Input foward sequence, should be same size as reverse',required=True)
parser.add_argument('-s','--seq_id', help='Input foward sequence, should be same size as reverse',required=True)

args = parser.parse_args()
inputfile=str(args.input)
seqid=str(args.seq_id)

output=inputfile.split(' ')
output='_'.join(output)

Entrez.email = "##################"
Entrez.api_key = 'a7309307bbdfdf2b45a5dedc6fdcce231509'

if not os.path.exists('New_Taxa/'):
        os.makedirs('New_Taxa/')
        
def get_tax_id(species):
    """to get data from ncbi taxomomy, we need to have the taxid. we can
    get that by passing the species name to esearch, which will return
    the tax id"""
    species = species.replace(' ', "+").strip()
    search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
    record = Entrez.read(search)
    try:
        got = record['IdList'][0]
        return record['IdList'][0]
    except IndexError:
        fout = open('Taxa_not_found.txt', 'w')
        fout.write(species)
        fout.close()
        
seq_id=open('seq2id.txt','w+')


"""Check to see if the taxa is in our dataset"""
for line in open(inputfile, "r"):
    taxid=get_tax_id(line)
    if str(taxid) == 'None':
        pass
    else:
        df= pandas.read_table(seqid, sep='    ',header = None )
        df[1]=df[1].astype('str')
        searchex=taxid+'.0'
        presentID = df[df[1].str.contains(searchex, regex=True)]

        """Get accession number of IdList"""
        if presentID.empty:
            fasta_fixed={}
            tmp='_'.join(line.split())
            print(line.strip('\n') + ' is empty with taxid '+taxid +'. Will now download fasta.')
            output=open('New_Taxa/'+tmp+".txt",'a')
            search = "txid"+taxid+"[Organism]"
            handle = Entrez.esearch(db="nucleotide", retmax=10, term=search, idtype="acc")
            record = Entrez.read(handle)
            record = record['IdList']

            """Get Fasta files and reformat into centrifuge fasta"""
            for acc_num in record:
                seq2id = acc_num+'    '+taxid
                seq_id.write(acc_num+'    '+taxid+'\n')
                handle = Entrez.efetch(db="nuccore", id=acc_num, rettype="fasta", retmode="text")
                for line in handle:
                    if line.startswith('>'):
                        line2=line
                        fasta_fixed[line2]=''
                        continue
                    fasta_fixed[line2]+=line
            count=0
            for key, value in fasta_fixed.iteritems() :
                if count==0:
                    output.write(key)
                    count+=1
                else:
                    output.write("\n"+key)
                output.write(value.strip('\n'))
        else:
            print(line.strip('\n') + ' is present with taxid '+taxid)
output.close()    
print('done')
