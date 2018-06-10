#will need to updateit, but wuick script to compare two files and print out lines that match and lines that do not in different files. I wanted to see what barcodes are present in my file and which are missing comapred to all the barcodes I have

import re


fout=open("matched.txt", 'w')
fout2=open("nomatch.txt", 'w')


with open("myfile.txt") as f1,open("totalplates.txt") as f2:
    words=set(line.strip() for line in f1)   #create a set of words from dictionary file
 
    for line in f2:
        word,freq=line.split() #fetch word,freq 
        if word in words:        #if word is found in words set then print it
            fout.write(word+'\n')
        else:
            fout2.write(word+'\n')

            
fout.close()
fout2.close()
