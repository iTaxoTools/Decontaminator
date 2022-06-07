##### Version 1.0 ######
#### David Leiße #######
##### david.leisse@uni-bielefeld.de #####

from genericpath import isdir
from os import listdir, mkdir
from os.path import splitext, isfile, join
import sys

__usage__ = """
    python3 decontamination.py
    --dir <PATH_TO_INPUT_FOLDER>
"""


def get_files(directory: str) -> list:
    """
    Getting all .ali and .log files from the input directory.

    :param String directory: Path to input directory.
    :return ali: list with all paths to .ali files
    :return log: list with all paths to .log files
    """

    onlyfiles = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
    ali = [f.split("/")[-1] for f in onlyfiles if splitext(f)[-1] == ".ali"]
    ali.sort()
    log = [f for f in onlyfiles if splitext(f)[-1] == ".log"]
    log.sort()

    return ali, log

def sanity_check(ali,log):
    """
    Checking if there are the same number of .ali files and .log files.

    :param List ali: list with all paths to .ali files
    :param List log: list with all paths to .log files
    """
    
    if not len(ali) == len(log):
        sys.exit("There are not an equal number of .ali files and .log files!!")

def parse_files(directory, file) -> dict:
    """
    Parsing .ali file and putting IDs corresponding to their sequence into a dictionary

    :param String file: Path to file
    :return file_dic: dictionary with IDs as key and the corresponding sequence as value.
    """
    file = directory + "/" + file

    with open(file, "r") as f:
        line = f.readline()

        duplicates = []
        sequence = []
        header = ""
        file_dic = {}
        while line:
            if line.startswith(">"):

                if sequence and header:
                    if header in file_dic:
                        duplicates.append(header)
                    file_dic[header] = sequence
                
                sequence = []
                header = line[1:86].strip()
            
            else:
                sequence.append(line)

            line = f.readline()

    return file_dic, duplicates

def log_task(log, ali_dic, duplicates):
    """
    Reading corresponding .log file and executing tasks: remove_seq

    :param String log: Path to corresponding log file
    :param Dictionary ali_dic: Dictionary with parsed .ali file
    :param List duplicates: List of duplicate sequence names that might have occured by shorting the name
    :return mod_ali: modified Dictionary
    """
    mod_ali_dic = ali_dic.copy()

    task_dic = {}
    with open(log, "r") as f:
        line = f.readline()
        while line:
            line = line.strip().split(" ")
            task_dic[" ".join(line[1:3]).replace('"',"")] = line[0]
            line = f.readline()


    relevant_duplicates = []
    for id,task in task_dic.items():
        if id in duplicates:
            relevant_duplicates.append(id)
        if task == "remove_seq":
            mod_ali_dic.pop(id)
    
    return mod_ali_dic, relevant_duplicates

def write_output(mod_ali_dic, ali_file, outputdirectory):
    """
    Writing output files from modified dictionary

    :param Dictionary mod_ali_dic: modified Dictionary with contents for decontaminated .ali files
    :param String ali_file: path to original .ali file
    """
    
    filename = outputdirectory + "/" + ali_file
    with open(filename, "w") as out:
        out.write("#\n")
        out.write("#\n")
        for id,seq in mod_ali_dic.items():
            out.write(">" + id + "\n")
            out.write(seq[0])

def __Main__(args):
    if type(args) == str:
        args = args.strip().split(" ")
    directory = args[args.index("--dir") +1]
    output_directory = directory + "/decontaminated"

    if not isdir(output_directory):
        mkdir(output_directory)

    duplicates = {}

    ali, log = get_files(directory)
    sanity_check(ali, log)
    for idx,entry in enumerate(ali):
        if idx == 4:
            print(entry)
        print(idx)
        ali_dic, duplicates_ls = parse_files(directory, entry)
        mod_ali_dic, relevant_duplicates_ls = log_task(log[idx], ali_dic, duplicates_ls)
        if relevant_duplicates_ls:
            duplicates[entry] = relevant_duplicates_ls
        if not mod_ali_dic == ali_dic:
            write_output( mod_ali_dic, entry, output_directory)

    if duplicates:
        print("Some duplicates have occured during the process")
        print("This has occured due to the shortening of sequence names in log files (max 85 char.)")
        for file, sequenceids in duplicates.items():
            print("In file " + file + " these sequence names have duplicates: " + str(sequenceids))

__Main__("--dir Testdaten2")

if not sys.argv:
    print("")

elif "--dir" in sys.argv:
    __Main__(sys.argv)

else:
    print(__usage__)