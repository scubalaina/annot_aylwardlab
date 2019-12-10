#!/bin/sh
#PBS -N output_dbase_hmmsearch
#PBS -m bea
#PBS -M anemail
#PBS -j oe
#PBS -A aylwardlab
#PBS -W group_list=cascades

#PBS -q normal_q
#PBS -l nodes=2:ppn=32
#PBS -l mem=16GB
#PBS -l walltime=100:0:0

cd current_working_directory

/home/alainarw/Tools/hmmer-3.2.1/src/hmmsearch -E evalue --tblout outdir/output_dbase_hmm.txt /groups/Aylward_Lab/HMM_databases/dbase.hmm proteins > outdir/output_dbase_hmm.out

rm outdir/output_dbase_hmm.out
