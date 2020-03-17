# Random_code_4_data_processign
## Listtle snips of code of which I have found useful but need to intergrate it into a larger set of codes

#randomly subsampling k number of reads from 2 fastq files
http://userweb.eng.gla.ac.uk/umer.ijaz/bioinformatics/subsampling_reads.pdf
```bash
paste in745_1_R1.fastq in745_1_R2.fastq | awk '{ printf("%s",$0); n++;if(n%4==0) { printf("\n");} else { printf("\t");} }' | awk -v k=10000 'BEGIN{srand(systime() + PROCINFO["pid"]);}{s=x++<k?x-1:int(rand()*x);if(s<k)R[s]=$0}END{for(i in R)print R[i]}' |awk -F"\t" '{print $1"\n"$3"\n"$5"\n"$7 > "in745_100k_R1.fastq";print $2"\n"$4"\n"$6"\n"$8 > "in745_100k_R2.fastq"}'
```

## Downlaoding from SRA with fasterq

install [SRA-Toolkit](https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit)

```bash
fasterq-dump  --outdir ~/SRA_COVID19/  -t ~/sra/  -e 16   -S   --skip-technical SRR11140750
```
