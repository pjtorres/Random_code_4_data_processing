__author__= 'Pedro J. Torres - 2018 '
import subprocess
import os,argparse

#--------Command line arguments------------------------------------------------------------------------------------
parser=argparse.ArgumentParser(description="Script allows you to count the number of raw reads in a given fastq.gz file ")
parser.add_argument('-i','--input', help='Input foward sequence, should be same size as reverse',required=True)

args = parser.parse_args()
inputfile=str(args.input)

name=inputfile
end=name.split(".")[-1]
name=name.split("R")[0]

adj='False'
if end == 'gz':
    try:
        output = open('RawSeqReads.txt','r')
        x='True'
        adj = "True"
    except IOError:
         output=open("RawSeqReads.txt",'wr+')
         batcmd= "zcat " + inputfile + " | grep -c @"
         result= subprocess.check_output(batcmd, shell=True)
         output.write("FileName " +"\t"+ "rawseq" +"\n"+name + '\t' + result)
         output.close()
        
    if adj =='True':
        output=open("RawSeqReads.txt",'a')
        batcmd= "zcat " + inputfile + " | grep -c @"
        result= subprocess.check_output(batcmd, shell=True)
        output.write(name + '\t' + result)
        output.close()
    else:pass

if end == 'fastq':
    try:
        output = open('RawSeqReads.txt','r')
        x='True'
        adj = "True"
    except IOError:
         output=open("RawSeqReads.txt",'wr+')
         batcmd= "cat " + inputfile +" | grep -c @"
         result= subprocess.check_output(batcmd, shell=True)
         output.write("FileName " +"\t"+ "rawseq" +"\n"+name + '\t' + result)
         output.close()
        
    if adj =='True':
        output=open("RawSeqReads.txt",'a')
        batcmd= "cat " + inputfile + " | grep -c @"
        result= subprocess.check_output(batcmd, shell=True)
        output.write(name + '\t' + result)
        output.close()
    else:pass
             
print('done')
