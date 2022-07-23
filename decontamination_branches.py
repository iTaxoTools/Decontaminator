### Decontamination Tool 2.0 ###
### David Leiße ###
### david.leisse@uni-bielefeld.de###

import shutil
import Utils
import dendropy as den
import os.path
import sys
import glob
from itertools import chain
import shutil

__Usage__ = """
            blub
"""

def get_long_edges(tree, threshhold, mode):
    leafs = []
    if mode == "internal":
        ls = den.Tree.internal_edges(tree)
    elif mode == "terminal":
        ls = den.Tree.leaf_edges(tree)
    else:
        sys.exit("Please select mode between 'internal' and 'terminal'")

    for edge in ls:
        if edge.length:
            if edge.length >= threshhold:
                node = edge.head_node
                for leaf in node.leaf_iter():
                    leafs.append(leaf.taxon)
                
    return leafs

def remove_seqs(leafs: list, seqs: list):
    modified_seqs = seqs.copy()
    for entry in leafs:
        label = entry.label.replace(" ","_")
        modified_seqs = [i for i in modified_seqs if not label == i[0]]

    return modified_seqs

def __Main__(args):

    if type(args) == str:
        args = args.strip().split(" ")

    dir_path = args[args.index("--dir") +1]
    threshhold = float(args[args.index("--thresh") +1])
    mode = args[args.index("--mode") +1]

    tre_files = glob.glob(dir_path + "/*.tre")
    ali_files = glob.glob(dir_path + "/*.ali")
    fasta_files = [glob.glob(dir_path + "/*.fas")]
    fasta_files.append(glob.glob(dir_path + "/*.fasta"))
    fasta_files = [x for x in chain(*fasta_files)]

    file_list = Utils.get_corresponding_files(tre_files,ali_files,fasta_files)

    for files in file_list:
        tree = Utils.load_tree(files[0], "path", "newick")
        if len(files) > 1:
            dest = os.path.join(dir_path, "decontaminated" ,os.path.basename(files[0]))
            shutil.copy(files[0], dest)

        leafs = get_long_edges(tree,threshhold, mode)
        for seq_file in files[1:]:

            filename = os.path.basename(seq_file)
            seqs = Utils.load_fasta_ali_file(seq_file)
            print("length: " + str(len(seqs)))

        
            modified_seqs = remove_seqs(leafs, seqs)
            print("length: " + str(len(modified_seqs)))
            Utils.write_decont_output(dir_path, filename, modified_seqs, type="nucleotides")

if not sys.argv:
    print("")

elif "--dir" in sys.argv and "--thresh" in sys.argv and "--mode" in sys.argv:
    __Main__(sys.argv)

else:
    print(__Usage__)
