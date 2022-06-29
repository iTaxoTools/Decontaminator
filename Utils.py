##### Utils.py #####
##### David Leiße #####
##### david.leisse@uni-bielefeld.de #####

import dendropy
from os import mkdir
from genericpath import isdir

def load_tree(string, mode, schema) -> dendropy.Tree:
    """
    Loading tree from .tre file and plotting it.
    Working with Newick schema until now.

    :param String string: Relative or absolute path to .tre file or data string
    :param String mode: Choosing between 'path' and 'string'
    :param String schema: I.e. 'newick' or 'nexus' depending on .tre file

    :return tree: Dendropy.Tree object
    """
    if mode == "path":
        tree = dendropy.Tree.get(path = string, schema = schema)
    elif mode == "string":
        tree = dendropy.Tree.get(data = string, schema = schema)
        
    return tree

def load_ali_file(file) -> list[str,str]:
    """
    Parsing .ali file and putting IDs corresponding to their sequence into a list

    :param String file: Path to file
    :return ls: list of lists with each an Sequence ID and the corresponding sequence.
    """

    with open(file, "r") as f:
        line = f.readline()

        sequence = []
        header = ""
        ls = []
        while line:
            if line.startswith(">"):

                if sequence and header:
                    temp = "".join(sequence).rstrip("\n")
                    ls.append([header, temp])
                
                sequence = []
                header = line[1:86].strip()
            
            else:
                sequence.append(line)

            line = f.readline()

    return ls

def load_fasta_ali_file(file) -> list[str,str]:
    """
    Loading fasta file into list. List containing lists with each an ID and sequence

    :param String file: full path to file
    :return ls: List containing lists with each an ID and sequence  
    """

    with open(file, "r") as f:
        line = f.readline()

        sequence = []
        header = ""
        ls = []
        while line:
            
            while line and not line.startswith(">"):
                if not sequence == "\n":
                    sequence.append(line.strip())
                line = f.readline()

            if sequence and header:
                ls.append([header, "".join(sequence)])
                
            sequence = []
            header = line[1:].strip()
            line = f.readline()
    
    return ls

def write_decont_output(directory, file, seq_ls, type):
    """
    Writing output files from modified dictionary

    :param List mod_ali_ls: modified list with contents for decontaminated .ali files
    :param String ali_file: path to original .ali file
    """

    output_directory = directory + "/decontaminated"
    if not isdir(output_directory):
        mkdir(output_directory)

    file = output_directory + "/" + file 

    with open(file, "w") as out:
        if type == "protein":
            out.write("#\n#\n")
        for id,seq in seq_ls:
            out.write(">" + id + "\n")
            out.write(seq + "\n")