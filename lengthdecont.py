### Decontamination Tool 2.0 ###
### David Leiße ###
### david.leisse@uni-bielefeld.de###

import sys
import Utils
import re
from os import listdir
from os.path import isfile, join


__Usage__ = """
            python3 lengthdecont.py
            --dir <FULL_PATH_TO_INPUT_DIRECTORY>
            --thresh <FLOAT>
            --mode <STRING_'percentage'_OR_'absolute'>
            --type <STRING_'protein'_OR_'nucleotide'>

"""


def length_decont(threshhold, seq_ls, mode, type): 
    """
    Removes temporaly all noninformation data in a sequence and compares its 
    length with the length of the original sequence that includes noninformation data.
    If the length of the decontaminated sequence (in comparison with the original) lies under
    a set threshhold it gets removed from the sequences list.

    :param Float threshhold: A threshhold set by the user. An absolute or relative number.
    :param List seq_ls: A list with all sequences from current alignment (.ali) file.
    :param String mode: String defining if threshhold is a relative or absolute number. ("percentage" or "absolute")
    :param String type: String defining if sequences are containing aminoacids ("protein") or nucleotides ("nucleotide")

    :return filtered_seq_ls: List containing filtered sequences from alignment (.ali) file.
    """

    filtered_seq_ls = []
    popped_seqs = []
    for i in seq_ls:
        seq = i[1].lower()
        if type == "nucleotide":
            filtered_seq = re.sub('[^atgcryswkm]',"",seq)
        if type == "protein":
            filtered_seq = re.sub('[^arndcqeghilkmfpstwyvuo]',"",seq)

        if mode == "percentage":

            perc = len(filtered_seq) / len(seq)
            if threshhold < perc:
                filtered_seq_ls.append(i)
            else:
                popped_seqs.append(i)
        
        elif mode == "absolute":

            if threshhold < len(filtered_seq):
                filtered_seq_ls.append(i)
            else:
                popped_seqs.append(i)

    return filtered_seq_ls

def __Main__(args):
    directory = args[args.index("--dir") +1]
    threshhold = float(args[args.index("--thresh") +1])
    mode = args[args.index("--mode") +1]
    type = args[args.index("--type") +1]

    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    
    for file in files:
        if type == "protein":
            seq_ls = Utils.load_ali_file(directory + "/" + file)
        elif type == "nucleotide":
            seq_ls = Utils.load_fasta_file(directory + "/" + file)
        else:
            print("No correct type argument! Please choose between 'protein' and 'nucleotide'")
            sys.exit()
        
        filtered_seq_ls = length_decont(threshhold, seq_ls, mode, type)
        Utils.write_decont_output(directory, file, filtered_seq_ls, type)


if "--dir" in sys.argv and "--thresh" in sys.argv and "--mode" in sys.argv and "--type" in sys.argv:
    __Main__(sys.argv)
else:
    print(__Usage__)
