_author__= 'Pedro J. Torres - 2019 '
import subprocess
from Bio import SeqIO
import os,argparse
from Bio import Entrez
import re,time
import pandas, numpy
import urllib, urllib2
import subprocess

# pip install biopython
# python update_database.py -i newly_addd.txt -s seqtry.map
#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script allows you to count the number of raw reads in a given fastq.gz file ")
parser.add_argument('-i','--input', help='Input foward sequence, should be same size as reverse',required=True)
parser.add_argument('-s','--seq_id', help='Input foward sequence, should be same size as reverse',required=True)
parser.add_argument('-l','--location', help='You can automatically add to our current database. Just insert the location of t$

args = parser.parse_args()
inputfile=str(args.input)
seqid=str(args.seq_id)
og_fna_location=str(args.location)
                    
 output=inputfile.split(' ')
output='_'.join(output)

Entrez.email = "##################"
Entrez.api_key = 'a7309307bbdfdf2b45a5dedc6fdcce231509'

if not os.path.exists('New_Taxa/'):
        os.makedirs('New_Taxa/')

#get the term or taxiD to locate the fasta later        
def get_tax_id(species):
   """to get data from ncbi taxomomy, we need to have the taxid. we can
    get that by passing the species name to esearch, which will return
    the tax id"""
    time.sleep(1)
    species = species.replace(' ', "+").strip()
    search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
    record = Entrez.read(search)
    try:
        got = record['IdList'][0]
        return record['IdList'][0]
    except IndexError:
        pass
        fout = open('Taxa_not_found.txt', 'w')
        fout.write(species)
        fout.close()
        
seq_id_new=open('new_taxa_seq2id.map','a')

"""Check to see if the taxa is in our dataset"""
for line in open(inputfile, "r"):
    taxid=get_tax_id(line)
    if str(taxid) == 'None':
        pass
    else:
        df= pandas.read_table(seqid, sep='    ',header = None )
        df[1]=df[1].astype('str')
#        print(df[1])
        searchex=taxid#+'.0'
 #       print(searchex)
        presentID = df[df[1].str.contains(searchex, regex=True)]

        """Get accession number of IdList"""
        if presentID.empty:
            fasta_fixed={}
            tmp='_'.join(line.split())
            tmp=tmp.replace('/','_') # replace these characters or you will have trouble opening new txt file at times
            print(line.strip('\n') + ' is empty with taxid '+taxid +'. Will now download fasta.')
            output=open('New_Taxa/'+tmp+".fna",'a')
            search = "txid"+taxid+"[Organism]"
            """Get fasta information using the taxonID we got earlier"""
            handle = Entrez.esearch(db="nucleotide", retmax=10, term=search, idtype="acc")
            record = Entrez.read(handle)
            record = record['IdList']
            species =[]
            """Get Fasta files and reformat into centrifuge fasta"""
            count=0
            for acc_num in record:
                count+=1
                if count == 3:
                    time.sleep(1)
                    count=0
                    continue
                seq2id = acc_num+'    '+taxid
                seq_id_new.write(acc_num+'    '+taxid+'\n')
                
                handle = Entrez.efetch(db="nuccore", id=acc_num, rettype="fasta", retmode="text")
                records = SeqIO.parse(handle, 'fasta')
                filtered = (rec for rec in records if any(ch != 'N' for ch in rec.seq)) #filters out files with all N's
                SeqIO.write(filtered, output, "fasta")
                
        else:
            print(line.strip('\n') + ' is present with taxid '+taxid)
#output.close()
concat= "cat New_Taxa/*.fna >>  New_Taxa/ALL_taxa.fna"
os.system(concat)
print('All fna files were concatenated into a new file and can be found here New_Taxa/ALL_taxa.fna')

    
print('done')                
                    
             
