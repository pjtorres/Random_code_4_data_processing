__author__= 'Pedro J. Torres'

# Allows you to make sure your taxonomic header is the same length throughout taxonomy. Sometimes you get outputs from Blast in which 
#taxonomic lineage stops at class, but others at species, so this code will fill the rest of your taxonomy with the lowest taxonomic lineage
#known until it reaches a length of 7 (aka species level).


f= open("inputfile.txt").read().splitlines()# input file
fout=open('newheaders.txt','w+')#output file with new headers

print 'We are starting'
for line in f:# remeber to remove any commas you have inbetween the ';' character which seperates your taxonomic lineage. You can use the substitute function in excel =SUBSTITUTE(A271,",","")
    line=line.split(';')
    linelen=len(line)
    while linelen < 7:
        nle=len(line)
        name=line[nle-1]
        line.append(name)
        linelen+=1
    else:
        line=("\t".join(line))
        final=str(line)+'\n'
        #print final
        fout.write(final)
fin.close()
fout.close()
print 'Done'

