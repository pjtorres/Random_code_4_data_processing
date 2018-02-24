__author__= 'Pedro J. Torres'
import argparse
import os
import pandas,numpy

#-----------Command Line Arguments-----------------
parser=argparse.ArgumentParser(description="Script allows you to convert theyour diamond output into a relative abudnace with percent unique")
parser.add_argument('-i','--input', help=' Input txt file output from diamond',required=True)
parser.add_argument('-o','--out', help='Name of output file: jsut the mae e.g., "sample1_final"', required=True)#require later
args = parser.parse_args()
o_file=str(args.out)
inputfile=str(args.input) 


#take in file and read args will be above
df = pandas.read_table(inputfile, sep='\t', 
                  names = ["Id_VF_Bac", "qseqid", "length"])  

# set the index to be this and don't drop
df.set_index(keys=['qseqid'], drop=False,inplace=True)

# get a list of names
names=df['qseqid'].unique().tolist()

vf_gene={}
info=[]
#---- Reformatting the DIAMOND output to be able to manipulate it easier on pandas -----------
print ('start pt1')
for u_qseqid in names:# iterate through each individual qseqid
    df_u_qseqid=df.loc[df.qseqid==u_qseqid] # here i essentially split my df based on the qseqid 
    
    #get protein name
    protein= df_u_qseqid[df_u_qseqid.columns[0]].iloc[0].split('[')[0]
    protein=protein.split('   ')[1]
    
    #get length
    length= df_u_qseqid[df_u_qseqid.columns[2]].iloc[0]
    
    #below will split the datafrane ID from my VF and bacteria
    df_id_vf_bac=df_u_qseqid['Id_VF_Bac'].str.split(' ',1, expand=True).rename(columns={0:'ID', 1:'VF_Bacteria' })# split my single column of Gene Bacteria back into two different files
    df_id_vf_bac.drop(df_id_vf_bac.columns[[0]], axis=1, inplace=True)

    #below will split the datframe protein from bacteria
    df_vf_bac=df_id_vf_bac['VF_Bacteria'].str.split('[',1, expand=True).rename(columns={0:'VF', 1:'Bacteria'})
    
    #rename columns into a single name, some names within the hits are variable (e.g, periplasmic protein disulfide isomerase I vs. protein disulfide isomerase I)
    df_vf_bac['VF']=protein
    
    #below will split the datframe protein from bacteria
    df_id_vf_bac=df_vf_bac['Bacteria'].str.split(' ',0, expand=True).rename(columns={0:'Genus', 1:'Species' })# split my single column of Gene Bacteria back into two different files
    
    #concatinate only important
    df_id_vf_bac['Bacteria']=df_id_vf_bac["Genus"].map(str) + " " + df_id_vf_bac["Species"] # this drops stuff

    #concatinate ourVirulence factor, and new bacteria columns
    df_qseqid_vf_bacteria=pandas.concat([df_vf_bac['VF'], df_id_vf_bac['Bacteria']], axis=1)  
    
    # summarize and get percent unique match
    col=df_qseqid_vf_bacteria.groupby('Bacteria').count()
    col['Uniq']=col['VF']
    col['Percent_Unique_Match']=(col['Uniq']/col['Uniq'].sum()*100)
    col.sort_values(by=['Percent_Unique_Match'])
    col=col.sort_values(by=['Percent_Unique_Match'], ascending=False)
    
    #lets drop unimportant columns and just leave the Bacteria and Percent Unique match
    col=col.reset_index(level=['VF'])
    col.drop(col.columns[[1,2]], axis=1, inplace=True)
    bacteria= col[col.columns[0]].iloc[0]
    percentunique= col[col.columns[1]].iloc[0]
    
    #add above info to list and then add that to dictionary
    gene_organims=bacteria+';'+protein
    merged=[gene_organims, str(percentunique), str(length)]
    vf_gene[u_qseqid]=merged

#write out file this could very well end up being a tmp file
#workdir=os.getcwd()
o=open("tmp1.txt","w+")
o.write("qseqid"+"\t"+"Organims_Gene"+"\t"+"Percent_Unique_Hits" +"\t"+"Length" "\n")
for i in vf_gene:
    o.write(i+"\t"+"\t".join([(xx) for xx in vf_gene[i]])+"\n")
o.close()

##################################################
###This is part 2 of the script--------------
#################################################
print ('Strat pt2')
#take in file and read args will be above
df = pandas.read_table("tmp1.txt", sep='\t')  

#dont care about qseqid anymore so we will drop that
df.drop(df.columns[[0]], axis=1, inplace=True)

# set the index to be this and don't drop. Everything will revovle around the virulence gene as this is what we
# want to get abundace to as before
df.set_index(keys=['Organims_Gene'], drop=False,inplace=True)

# get a list of unique genes present in the directory
names=df['Organims_Gene'].unique().tolist()
print ('There are ' + str(len(names))+ ' unique organism/gene combinations')

# list and dictionary to add stuff to later
taxa={}
information=[]

for gene in names:# iterate trhough each individual qseqid
    df_u_gene=df.loc[df.Organims_Gene==gene] # here i essentially split my df based on the qseqid 
   # print df_u_gene

    #get length of gene
    length= df_u_gene[df_u_gene.columns[2]].iloc[0]

    #start grouping and getting relative abundances and unique hits
    df_u_gene_per=df_u_gene[['Organims_Gene','Percent_Unique_Hits']]
    df_u_gene_per['Abundance']=1
    col=df_u_gene_per.groupby(['Organims_Gene'])[["Percent_Unique_Hits","Abundance"]].sum()
    col['Percent_Unique_Hit']=(col['Percent_Unique_Hits']/col['Abundance'])
    col['Normal_abund']=(col['Abundance']/length)*10000 # multiplied by 10k to get larger numbers to work with in relative abudnace followed similar rules as FPKM
    
    #lets drop unimportant columns and just leave the Bacteria and Percent Unique match
    col=col.reset_index(level=['Organims_Gene'])
    organism_gene= col[col.columns[0]].iloc[0]
    percentunique= col[col.columns[3]].iloc[0]
    normal_abundance= col[col.columns[4]].iloc[0]
    
    #add above info to list and then add that to dictionary
    merged=[str(percentunique), str(normal_abundance)]     
    taxa[organism_gene]=merged

#write out file this could very well end up being a tmp file
o=open("tmp2.txt","w+")
o.write("Organism_gene"+"\t"+"Percent_Unique"+"\t"+"Normal_abundance" + "\n")
for i in taxa:
    o.write(i+"\t"+"\t".join([(xx) for xx in taxa[i]])+"\n")
o.close()
os.remove("tmp1.txt")# remove first temp file from before

############################################################
#### This is the last part of the script pt3 -----------------
############################################################


df = pandas.read_table("tmp2.txt", sep='\t')  
# set the index to be this and don't drop. Everything will revovle around the virulence gene as this is what we
# want to get abundace to as before
df.set_index(keys=['Organism_gene'], drop=False,inplace=True)
df['Relative_abundance']=(df['Normal_abundance'].div(df['Normal_abundance'].sum(axis=0)).multiply(100))
#lets drop unimportant columns and just leave the Bacteria and Percent Unique match
#col=col.reset_index(level=['VF'])
df.drop(df.columns[[2]], axis=1, inplace=True)
df=df.sort_values(by=['Organism_gene'], ascending=False)
df.to_csv(o_file+'.csv')
os.remove("tmp2.txt")

print ('Done :)')
