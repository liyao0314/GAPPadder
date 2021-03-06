import sys
import os
from subprocess import *
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def run_cmd(cmd1):
    #print cmd1
    check_output(cmd1, shell=True)

def merge_reads_v2(sf_fai, sf_gap_pos, merge_folder_list, reads_folder, n):

    if os.path.exists(reads_folder)==False:
        cmd="mkdir {0}".format(reads_folder)
        run_cmd(cmd)

    m_scaffold_id={}
    cnt=0
    with open(sf_fai) as fin_fai:
            for line in fin_fai:
                fields=line.split()
                scaffold_id=fields[0]
                m_scaffold_id[scaffold_id]=cnt
                cnt=cnt+1

    cmd_list=[]
    cnt=1
    pre_id=0
    with open(sf_gap_pos) as fin_gap_pos:#for each gap
        for line in fin_gap_pos:
            fields=line.split()
            scaffold=fields[3]
            scaffold_id=m_scaffold_id[scaffold]

            if pre_id!=scaffold_id:
                cnt=1

            sf_fq="{0}_{1}.fastq".format(scaffold_id,cnt)
            cnt=cnt+1
            pre_id=scaffold_id

            cmd="cat "
            for folder in merge_folder_list:
                sf_fq_x=folder+"/{0}/{1}".format(reads_folder, sf_fq)
                if os.path.exists(sf_fq_x)==True:
                    cmd=cmd+" {0}".format(sf_fq_x)

            if cmd!="cat ":
                cmd=cmd+" > {0}/{1}".format(reads_folder, sf_fq)
                cmd_list.append(cmd)

    pool = ThreadPool(n)
    pool.map(run_cmd, cmd_list)
    pool.close()
    pool.join()


if __name__ == "__main__":
    print "Merge reads..."
    merge_folder_list=[]
    merge_folder_list.append("./../long_jump_nx")
    merge_folder_list.append("./../short_insert")
    merge_folder_list.append("./../short_jump")
    #merge_folder_list.append("/data2/chongchu/Octopus_data/insert_size_3500")
    #merge_folder_list.append("/data2/chongchu/Octopus_data/insert_size_10k")


    merge_reads_v2(sys.argv[1],sys.argv[2], merge_folder_list, "gap_reads", int(sys.argv[3]))
    merge_reads_v2(sys.argv[1],sys.argv[2], merge_folder_list, "gap_reads_alignment", int(sys.argv[3]))
    merge_reads_v2(sys.argv[1],sys.argv[2], merge_folder_list, "gap_reads_high_quality", int(sys.argv[3]))