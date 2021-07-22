from Bio import SeqIO
input='GCA_006942135.1_ASM694213v1_genomic.fna'
keep='PQTP01000029.1'
out='tmp_GCA_006942135.1_ASM694213v1_genomic.fna'

wanted = (rec for rec in SeqIO.parse(input, "fasta") \
                        if rec.id.startswith(keep))
count = SeqIO.write(wanted, out, "fasta")
print ("Saved %i records" % count)

# keep a particular fasta in a multi fasta file beased on heaeder
