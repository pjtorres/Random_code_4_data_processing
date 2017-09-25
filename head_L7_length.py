# Allows you to make sure your taxonomic header is the same length throughout taxonomy. Sometimes you get outputs from Blast in which 
#taxonomic lineage tps at class, but others at species, so this code will fill the rest of your taxonomy with the lowest taxonomic lineage
#known until it reaches a length of 7 (aka species level).

f= open("try2.txt").read().splitlines()

fout=open('newheaders.txt','w+')
for line in f:  # remeber to remove any commas you can use the substitute function in excel!
    line=line.split(';')
    linelen=len(line)
#    print line
    while linelen != 7:
        nle=len(line)
        name=line[nle-1]
        line.append(name)
        linelen+=1
    else:
        line=("\t".join(line))
        final=str(line)+'\n'
        print final
        fout.write(final)

fout.close()
print "Done yo :)"
