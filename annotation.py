import os, argparse,subprocess, shlex

args_parser = argparse.ArgumentParser(description="Script for generating and running PBS scripts for HMM searches of proteisn against specified databases", epilog="Virginia Tech Department of Biological Sciences")
args_parser.add_argument('-i', '--input_prot', required=True, help='Input file of FAA sequences')
args_parser.add_argument('-d', '--db', required=True, nargs='+', help='Databases for matching. Type each database you would like to search against separated by spaces. ' 
	'Accepted entries are: cog, "nog", "vog", "pfam", "tigrfam", "eggvog", or "all". "all" searches all of these databases.')
args_parser.add_argument('-E','--EVALUE', required=False, default = str(10.0), help='Cutoff E-value for hmmsearch. Default is 0.001.')
args_parser.add_argument('-o','--output_name', required=False, default = "project", help='Prefix handle of output folder and output files.')
args_parser.add_argument('-email','--email', required=True, help='Email address for ARC to notify job initiation and completion.')
args_parser = args_parser.parse_args()

input_prot = args_parser.input_prot
db = args_parser.db
EVALUE = args_parser.EVALUE
output_name = args_parser.output_name
email = args_parser.email

cwd = os.getcwd()

out_dir = output_name + "_hmm_out"
os.mkdir(out_dir)

#print(db)
template = open("template.sh",'r')

filedata = template.read()
filedata = filedata.replace('current_working_directory',cwd)
filedata = filedata.replace('output',output_name)
filedata = filedata.replace('evalue',EVALUE)
filedata = filedata.replace('proteins',input_prot)
filedata = filedata.replace('outdir',out_dir)
filedata = filedata.replace('anemail',email)

output_list = []


for i in db:
	if i == "all":
		db = ['cog','nog','vog','eggvog','pfam','tigr']
else:
	pass

for i in db:
	filedata1 = filedata.replace("dbase",i)
	outputa = output_name + "_" + i + "_hmmsearch.sh"
	output_list.append(outputa)
	with open(outputa,'w') as file:
		file.write(filedata1)


for i in output_list:
	cmd = "qsub " + i
	cmd2 = shlex.split(cmd)
	print(cmd)
	subprocess.call(cmd2)
