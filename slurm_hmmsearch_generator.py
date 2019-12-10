import os, argparse,subprocess, shlex, re

args_parser = argparse.ArgumentParser(description="Script for generating and running PBS scripts for HMM searches of proteisn against specified databases", epilog="Virginia Tech Department of Biological Sciences")
args_parser.add_argument('-i', '--input_folder', required=True, help='Input file of FAA sequences')
args_parser.add_argument('-d', '--db', required=True, nargs='+', help='Databases for matching. Type each database you would like to search against separated by spaces. ' 
	'Accepted entries are: cog, "nog", "vog", "pfam", "tigrfam", "eggvog", or "all". "all" searches all of these databases.')
args_parser.add_argument('-E','--EVALUE', required=False, default = str(10.0), help='Cutoff E-value for hmmsearch. Default is 0.001.')
#args_parser.add_argument('-o','--output_name', required=False, default = "project", help='Prefix handle of output folder and output files.')
args_parser.add_argument('-email','--email', required=True, help='Email address for ARC to notify job initiation and completion.')
args_parser = args_parser.parse_args()

input_folder = args_parser.input_folder
db = args_parser.db
EVALUE = args_parser.EVALUE
#output_name = args_parser.output_name
email = args_parser.email
filename = ""

cwd = os.getcwd()
#print(cwd)
cwd = cwd + "/"

if input_folder.endswith("/"):
	pass
else:
	input_folder = input_folder + "/"

for filename in os.listdir(input_folder):
	if filename.endswith(".faa"):
		prefix_list = filename.split("/")
		prefix = prefix_list[len(prefix_list)-1]
		prefix2 = re.sub(".faa","",prefix)
		#print(prefix2)
		out_dir1 = cwd + input_folder + prefix2 + "_hmm_out"

		os.mkdir(out_dir1)
		out_dir = input_folder + prefix2 + "_hmm_out"

#print(db)
		template = open("slurm_hmmsearch_template.sh",'r')

		filedata = template.read()
		filedata = filedata.replace('current_working_directory',cwd)
		#print(prefix)

		filedata = filedata.replace('evalue',EVALUE)
		filedata = filedata.replace('proteins',filename)
		filedata = filedata.replace('outdir',out_dir)
		filedata = filedata.replace('Email',email)
		filedata = filedata.replace('prefix',prefix2)



		output_list = []


		for i in db:
			print(i)
			if i == "all":
				db = ['cog','nog','vog','eggvog','pfam','tigr']
			else:
				pass

		for i in db:
			filedata1 = filedata.replace("dbase",i)
			print(prefix2)
			outputa = cwd + input_folder + prefix2 + "_" + i + "_hmmsearch.sh"
			output_list.append(outputa)
			with open(outputa,'w') as file:
				file.write(filedata1)


		for i in output_list:
			cmd = "qsub " + i
			cmd2 = shlex.split(cmd)
			#print(cmd)
			#subprocess.call(cmd2)

