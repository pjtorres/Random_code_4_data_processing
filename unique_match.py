__author__= 'Pedro J. Torres'
import re,os,argparse

#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script allows you to compare two files and pull out ids that are similar in the first column of the file and add them to a new matched file while those that are unique are pulled into another unique file. You must have two columns in your files first in the column you wish to match or find unique and second is whatever else. Still need to update this to deal with any file.\n Files must be tab delimeted txt files! ")
parser.add_argument('-i1','--input_file1', help='Input first file you wish to be matched.',required=True)
parser.add_argument('-i2','--input_file2', help='Input second file you wish to be matched.',required=True)

args = parser.parse_args()
inputfile1=str(args.input_file1)
inputfile2=str(args.input_file2)

#this is the name of the oputput files
fout=open("matched.txt", 'w')
fout2=open("nomatch.txt", 'w')

with open(inputfile1) as f1,open(inputfile2) as f2:
    words=set(line.strip() for line in f1)   #create a set of words from dictionary file
    for line in f2:
        word,freq=line.split() #fetch word,freq 
        if word in words:        #if word is found in words set then print it
            fout.write(word+'\n')
        else:
            fout2.write(word+'\n')
        
fout.close()
fout2.close()

print('Done! :)')
print('Your folder should now have two files a 1. matched.txt and 2. nomatch.txt ')
