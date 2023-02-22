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
from os import mkdir
from genericpath import isdir
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import itertools as it
import gc
import logging


__Usage__ = """
            python3 decontamination_branches.py
            --dir <PATH_TO_INPUT_FOLDER>
            --thresh <FLOAT_EDGE_LENGTH_THRESHHOLD>
            --mode <"internal"_or_"terminal"_edge_iteration>
"""

def get_top_long_edges(tree: den.Tree, absolute: int, perc: float, mode: str) -> list:
    """
    Iterating through either internal or terminal branches of a Dendropy Tree.
    Sorting edges by length and selecting an absolute number or percentage of the longest branches and returning their descending leaf nodes.

    :param Dendropy.Tree tree: A dendropy.tree object from a .tre file
    :param Int absolute: Absolute number selected by user
    :param Float perc: Percentage in decimal format selected by user
    :param String mode: Selection between "internal" and "terminal" branches.

    """
    leafs = []
    if mode == "internal":
        ls = den.Tree.internal_edges(tree)
    else:
        ls = den.Tree.leaf_edges(tree)

    ls.sort(key = lambda x: x.length)

    if perc:
        absolute = 1-round(len(ls)*perc)
 
    for i in ls[:absolute]:
        for leaf_node in i.head_node.leaf_nodes():
            leafs.append(leaf_node.taxon.label)

    return leafs

def get_quantile_long_edges(mode: str, tree: den.Tree, quantile: float):

    leafs = []
    if mode == "internal":
        ls = den.Tree.internal_edges(tree)
    else:
        ls = den.Tree.leaf_edges(tree)

    lengths =[]
    for edge in ls:
        if edge.length:
            lengths.append(edge.length)

    cutoff = np.quantile(lengths, quantile)
    logging.info("Quantile cutoff: " + str(cutoff))

    for edge in ls:
        if edge.length:
            if edge.length > cutoff:
                #print(edge.length)
                node = edge.head_node
                for leaf in node.leaf_node_iter():
                    #print(leaf.taxon)
                    leafs.append(leaf.taxon.label)
    
    return leafs

def get_branch_lengths(tree: den.Tree):
    root_to_leaf_lengths = {}
    for leaf in tree.leaf_node_iter():
        root_to_leaf_lengths[leaf] = leaf.distance_from_root()

    """
    root_distance_sisters = []
    for pairs in sister_nodes:
        root_distance_temp = []
        root_distance_temp.append(pairs[0].taxon)
        if len(pairs) > 2:
            print("stop")
        for i in pairs:
            if type(i) == list:
                temp = []
                for j in i:
                    temp.append(j.distance_from_root())
                root_distance_temp.append(np.mean(temp))
            else:
                root_distance_temp.append(i.distance_from_root())
        
        root_distance_sisters.append(root_distance_temp)
    """
    return root_to_leaf_lengths

def get_factor_long_edges(tree: den.Tree, factor: float):

    sisters = Utils.get_sister_nodes(tree)
    branch_lengths = get_branch_lengths(tree)
    long_leafs = []
    for i in sisters:
        leaf = branch_lengths[i[0]]
        if type(i[1]) == list:
            ref = np.mean([branch_lengths[x] for x in i[1]])
        else:
            ref = branch_lengths[i[1]]
        ref = ref * factor
        if leaf >= ref:
            long_leafs.append(i[0].taxon.label)
    
    return long_leafs

def compare_trees(tree: den.Tree, reference_tree: den.Tree):
    missing_taxa = []
    for i in reference_tree.taxon_namespace.labels():
        if not tree.taxon_namespace.get_taxon(i):
            missing_taxa.append(i)

    return missing_taxa

def normalizing_values(dic: dict):
    rel_dic = {}
    rel = np.mean([y for y in dic.values()])
    for key,value in dic.items():
        rel_val = value / rel
        rel_dic[key] = rel_val

    return rel_dic

def get_reference_tree_long_edges(tree: den.Tree, reference_tree: den.Tree, factor: float):
    #----------- comparing trees and adjusting reference tree ------------------#
    too_many_taxa_in_reference = compare_trees(tree, reference_tree)
    try:
        reference_tree.prune_taxa(too_many_taxa_in_reference)
    except AttributeError:
        logging.warning("___________________________________________")
        logging.warning("!!!!!!!Reference tree does not contain any taxa from testtree!!!!!!!")
        logging.warning("___________________________________________")

    missing_taxa_in_reference = compare_trees(reference_tree, tree)
    #returne warning if taxa that exist in testtree are missing in reference tree#
    if missing_taxa_in_reference:
        logging.warning("___________________________________________")
        logging.warning("!!!!Taxa are missing in reference tree!!!!!")
        for i in missing_taxa_in_reference:
            logging.info("Ignoring " + i)

    #----------- Getting all branch lengths ------------------------------------#

    reference_lengths = {}
    [reference_lengths.update({x.taxon.label : x.distance_from_root()}) for x in reference_tree.leaf_node_iter()]
    tree_lengths = {}
    [tree_lengths.update({x.taxon.label : x.distance_from_root()}) for x in tree.leaf_node_iter()]

    #----------- calculating normalized branchlength ----------------------------#
    normalized_reference = normalizing_values(reference_lengths)
    normalized_tree = normalizing_values(tree_lengths)

    #----------- comparing branch lengths of same taxa --------------------------#
    long_leafs = []
    for key,value in normalized_tree.items():
        if key in normalized_reference:
            ref = normalized_reference[key]
            if ref*factor < value:
                long_leafs.append(key)


    return long_leafs

def remove_seqs(leafs: list, seqs: list, file: str) -> list:
    """
    Removing sequences and their name from the list, if names are contained in the leaf list from "get_long_edges"

    :param List leafs: List of leaf node labels (from get_long_edges)
    :param List seqs: List of sequences and their names from a .fasta or .ali file
    :return modified_seqs: Modified list of sequences and their names from a .fasta or .ali file.
    """
    
    modified_seqs = seqs.copy()
    for entry in leafs:
        label = entry.strip().replace(" ","_")
        modified_seqs = [i for i in modified_seqs if not label == i[0]]
        logging.info("Removed " + label + " from alignmentfile: '" + file +  "'.")

    return modified_seqs

def decontaminate_files(target: str, files: list, leafs:list, dest: str, tree: den.Tree):

    if target == "alignment" or target == "both":
        for seq_file in files[1:]:
            filename = os.path.basename(seq_file)
            seqs = Utils.load_fasta_ali_file(seq_file)
            print("length of " + str(filename) + " before: " + str(len(seqs)))

        
            modified_seqs = remove_seqs(leafs, seqs, filename)
            print("length of " + str(filename) + " after: " + str(len(modified_seqs)))
            Utils.write_decont_output(dest, filename, modified_seqs, type="nucleotides", folder="")

    if target == "tree" or target == "both":
        filename = os.path.basename(files[0])

        print("Number of taxa in " + filename + " :" + str(tree.__len__()))
        tree.prune_taxa_with_labels(leafs)
        print("Number of taxa in " + filename + " after pruning :"  + str(tree.__len__()))
        
        if not isdir(dest):
            mkdir(dest)
        tree.write_to_path(dest + "/" + filename, schema= "newick")
    
    if target == "alignment":
        shutil.copy(files[0], dest)
    elif target == "tree":
        for i in files[1:]:
            shutil.copy(i, dest)

def __Main__(cmdline):

#--------------- Initialize Logger ------------------------#
    logging.basicConfig(filename = "logfile.log", format="%(asctime)s %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.info("----------- New process started --------------")


#--------------- Processing command line ------------------#
    if type(cmdline) == str:
        cmdline = cmdline.strip().split(" ")

    arg_list = ["dir","mode","target","perc","absolute","quantile","factor","referencetree"]
    defaults = ["","","alignment",0,0,0,0,""]

    dir_path, mode, target, perc, absolute, quantile, factor, referenceTree, loggingstr = Utils.process_cmd_arguments(defaults, arg_list, cmdline)
    logging.info("Parameters: \n" + loggingstr)


    outpath = os.path.join(dir_path, "decontaminated")
    if not isdir(outpath):
        mkdir(outpath)

    tre_files = glob.glob(dir_path + "/*.tre")
    ali_files = glob.glob(dir_path + "/*.ali")
    fasta_files = [glob.glob(dir_path + "/*.fas")]
    fasta_files.append(glob.glob(dir_path + "/*.fasta"))
    fasta_files = [x for x in chain(*fasta_files)]

    dataset_list = Utils.get_corresponding_files(tre_files,ali_files,fasta_files)

#--------------- Decontaminating Dataset by Dataset --------------#

    for dataset in dataset_list:
        logging.info("Dataset: " + os.path.splitext(os.path.basename(dataset[0]))[0])

        tree = Utils.load_tree(dataset[0], "path", "newick")
        if len(dataset) > 1:
            dest = os.path.join(dir_path, "decontaminated")

            if absolute or perc:
                leafs = get_top_long_edges(tree, int(absolute), perc, mode)
            elif quantile:
                leafs = get_quantile_long_edges(mode, tree, quantile)
            elif referenceTree:
                referenceTree = Utils.load_tree(referenceTree, "path", "newick")
                leafs = get_reference_tree_long_edges(tree, referenceTree, factor)
            elif factor:
                leafs = get_factor_long_edges(tree, factor)

            decontaminate_files(target, dataset, leafs, dest, tree)
            logging.info("")

if not sys.argv:
    print("")

elif "--dir" in sys.argv and "--mode" in sys.argv:
    __Main__(sys.argv)

else:
    print(__Usage__)
