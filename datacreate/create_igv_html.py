import pandas as pd
import subprocess
import os

def create_html(name, df):
    for index, row in df.iterrows():
        genome_site = row['genome_site']
        common = row['common']

        index_name = name + "_" + str(index)
        # bed_line = name + "\t" + str(genome_site) + "\t" + str(genome_site) + "\t" + common  # 內文
        bed_line = "gi|556503834|ref|NC_000913.3|\t" + str(genome_site -1 ) + "\t" + str(genome_site) + "\t" + common  # 內文

        with open("/home/xiangwei/chien/rnafold/datacreate/tmp.bed",'w') as file:
            file.write(bed_line)

        command = f"create_report /home/xiangwei/chien/rnafold/datacreate/tmp.bed --fasta /home/xiangwei/chien/rnafold/datacreate/Data/E.coli_BCM_treatment_bam_files_new/E.coli_reference_genome/NC_000913_spikeRNA.fna --flanking 50 --tracks /home/xiangwei/chien/rnafold/datacreate/Data/E.coli_BCM_treatment_bam_files_new/S08_11_BLM_log_3L.bowtie2mapping.rRNA_filtered_sorted.bam /home/xiangwei/chien/rnafold/datacreate/Data/E.coli_BCM_treatment_bam_files_new/S09_09_WT_log_3L.bowtie2mapping.rRNA_filtered_sorted.bam --output /home/xiangwei/chien/rnafold/datacreate/IGV/{name}_html/{index_name}.html"

        subprocess.run(command, shell=True, text=True)
        # os.system(command)

        try:
            # 将文件移动到 'pictures' 文件夹
            os.rename(f"{index_name}.html", f"/home/xiangwei/chien/rnafold/datacreate/IGV/{name}_html/{index_name}.html")
        except FileNotFoundError:
            pass  # 处理文件不存在的情况

        print(index)



if __name__ == "__main__":
    name = "S08_11"
    site_data = pd.read_csv(f"{name}_common.csv")

    create_html(name, site_data)