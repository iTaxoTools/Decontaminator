##### Version 1.0 ######
#### David Leiße #######
##### david.leisse@uni-bielefeld.de #####

from genericpath import isdir
from os import listdir, mkdir
from os.path import splitext, isfile, join, basename
from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
import sys

from itaxotools.decontaminator import Utils

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
    ali = [basename(f) for f in onlyfiles if splitext(f)[-1] == ".ali"]
    ali.sort()
    log = [basename(f) for f in onlyfiles if splitext(f)[-1] == ".log"]
    log.sort()
    index = len(log)
    if not len(log) == len(ali):
        lengths = [len(log),len(ali)]
        index = lengths[lengths.index(min(lengths))]


    return ali[:index], log[:index]

def sanity_check(ali,log):
    """
    Checking if there are the same number of .ali files and .log files.

    :param List ali: list with all paths to .ali files
    :param List log: list with all paths to .log files
    """
    
    if not len(ali):
        print("There were no ali files found")
    elif not len(log):
        print("There were no log files found")
    elif not len(ali) == len(log):
        print("There are not an equal number of .ali files and .log files!!")

# def parse_files(directory, file) -> list:
#     """
#     Parsing .ali file and putting IDs corresponding to their sequence into a list

#     :param String file: Path to file
#     :return ls: list of lists with each an Sequence ID and the corresponding sequence.
#     """
#     file = directory + "/" + file

#     with open(file, "r") as f:
#         line = f.readline()
        
#         sequence = []
#         header = ""
#         ls = []
#         while line:
#             if line.startswith(">"):

#                 if sequence and header:
#                     ls.append([header, sequence])
                
#                 sequence = []
#                 header = line[1:86].strip()

#             else:
#                 sequence.append(line)

#             line = f.readline()

#     return ls

def log_task(commands: dict, ali_ls: list):
    """
    Reading corresponding .log file and executing tasks: remove_seq, extract_seq

    :param String log: Path to corresponding log file
    :param List ali_ls: List with parsed .ali file
    :return mod_ali: modified .ali file list
    """
    mod_ali_ls = ali_ls.copy()
    extracted_seqs = []

    relevant_duplicates = []
    for id,task in commands.items():
        if task == "remove_seq":
            print("remove " + str(id))
            idx_ls = [idx for idx,i in enumerate(mod_ali_ls) if id in i]
            if len(idx_ls) >= 2:
                    relevant_duplicates.append(id)
            for idx in idx_ls:
                mod_ali_ls.pop(idx)
        
        elif task == "extract_seq":
            idx_ls = [idx for idx,i in enumerate(ali_ls) if id in i]
            for idx in idx_ls:
                extracted_seqs.append(ali_ls[idx])

    
    return mod_ali_ls, relevant_duplicates, extracted_seqs

def write_output(mod_ali_ls, ali_file, directory, output_directory):
    """
    Writing output files from modified dictionary

    :param List mod_ali_ls: modified list with contents for decontaminated .ali files
    :param String ali_file: path to original .ali file
    """

    output_directory = join(directory, output_directory)
    file = join(output_directory, ali_file)

    if not isdir(output_directory):
        mkdir(output_directory)
    
    with open(file, "w") as out:
        out.write("#\n")
        out.write("#\n")
        for id,seq in mod_ali_ls:
            out.write(">" + id + "\n")
            out.write(seq + "\n")

def __Main__(args):
    if type(args) == str:
        args = args.strip().split(" ")
    
    directory = args[args.index("--dir") +1]

    duplicates = {}

    ali, log = get_files(directory)
    sanity_check(ali, log)
    for idx,entry in enumerate(ali):
        print("Processing file number: " + str(idx+1))
        filepath = join(directory, entry)
        ali_ls = Utils.load_fasta_ali_file(filepath, change=False)
        logpath = join(directory,log[idx])
        commands = Utils.load_log_commands(logpath)
        mod_ali_ls, relevant_duplicates_ls, extracted_ls = log_task(commands, ali_ls)
        if relevant_duplicates_ls:
            duplicates[entry] = relevant_duplicates_ls
    
        write_output(mod_ali_ls, filepath, directory, "decontaminated")

        if extracted_ls:
            write_output(extracted_ls, filepath, directory, "extracted")

    if duplicates:
        print("Some duplicates have occured during the process")
        print("This has occured due to the shortening of sequence names in log files (max 85 char.)")
        for file, sequenceids in duplicates.items():
            print("In file " + file + " these sequence names have duplicates: " + str(sequenceids))

def run():
    if not sys.argv:
        print("")

    elif "--dir" in sys.argv:
        __Main__(sys.argv)

    else:
        print(__usage__)
