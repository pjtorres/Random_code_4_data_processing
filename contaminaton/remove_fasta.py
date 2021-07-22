from Bio import SeqIO
input='tmpdna.fas'
remove='GG692418.1' 
out='tmpdna_filtered.fas'

wanted = (rec for rec in SeqIO.parse(input, "fasta") \
                        if not rec.id.startswith(remove))
count = SeqIO.write(wanted, out, "fasta")
print ("Saved %i records" % count)

# remove aprticular fasta from fasta header
