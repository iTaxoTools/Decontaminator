#### rename_seq #####
import Utils
import glob
import os
import sys

__usage__ = """
        python3 remove_rename.py
        --dir <PATH_TO_INPUT_FOLDER>
"""


def read_command_file(file: str) -> list:
    """
    Parsing command .txt / .log file into a dictionary: "text":"command"

    :param String file: Path to file
    :return commands: Dictionary with commands and corresponding text
    """
    
    commands = []
    characters = ["@"," "]
    with open(file, "r") as f:
        line = f.readline()

        while line:
            if not line == "\n":
                parts = line.strip().split(" ")
                command = parts[0]
                name = "_".join(parts[1:])
                for character in characters:
                    name = name.replace(character,"_")
                commands.append([name, command])
            
            line = f.readline()


    return commands

def commands_processing(commands: list) -> dict:
    """
    Sorting and processing commandlines by command

    :param Dictionary commands: Dictionary with commands and corresponding text

    :return Dictionary rem_commands: Dictionary with all remove commands
    :return Dictionary ren_commands: Dictionary with all rename commands
    :return Dicitonary repin_commands: Dictionary with all replace_in commands
    :return Dictionary trim_commands: Dictionary with all trim commands
    """
    rem_commands = {}
    extr_commands = {}
    ren_commands = {}
    repin_commands = {}
    trim_commands = []
    for name,command in commands:
        if command == "remove_seq":
            s_name = name.replace('"',"")[:-1]
            rem_commands[s_name] = command
        
        elif command == "extract_seq":
            e_name = name.replace('"',"")[:-1]
            extr_commands[e_name] = command
            
        elif command == "rename_seqname":
            names =  name.split('"')
            indices = [1,3]
            l_names = ";".join([names[x] for x in indices])
            ren_commands[l_names] = command
        
        elif command == "replacein_seqname":
            names = name.split('"')
            indices = [1,3]
            l_names = ";".join([names[x] for x in indices])
            repin_commands[l_names] = command
        
        elif "trim" in command:
            name = name.replace('"',"")[:-1]
            trim_commands.append([name,command])
        
        else: print("Your command " + command + "does not seem to be correct. Please check your command file again.")

    return rem_commands, extr_commands, ren_commands, repin_commands, trim_commands

def remove_seq(commands: dict, data: list) -> list:
    """
    Removing sequences and their names from data list by command.

    :param Dictionary commands: All remove commands and the corresponding text
    :param List data: List of sequence names and the corresponding sequences

    :return data_removed: Modified data list with specifically removed sequences
    """
    data_removed = data.copy()
    for name,command in commands.items():
         if command =="remove_seq":
            try: 
                index = Utils.get_index_in_list(name, data_removed)
                if index:
                    print("stop")
                data_removed.pop(index)

            except: print(name + "has not been found in ")

    return data_removed

def extract_seq(commands: dict, data:list) -> list:
    """
    Extracting sequences and their names from data list by command.

    :param Dictionary commands: All remove commands and the corresponding text
    :param List data: List of sequence names and the corresponding sequences

    :return data_extracted: Modified data list with specifically extracted sequences
    """
    data_extracted = []
    for name,command in commands.items():
        if command == "extract_seq":
            try:
                index = Utils.get_index_in_list(name, data)
                data_extracted.append(data[index])
            
            except: print(name + "has not been found")
                

    return data_extracted

def rename_seq(commands: dict, data: list) -> list:
    """
    Renaming sequence names in data list by command.

    :param Dictionary commands: All rename commands and the corresponding text
    :param List data: List of sequence names and the corresponding sequences

    :return data_renamed: Modified data list with specifically renamed sequence names
    """

    data_renamed = data.copy()
    for name, command in commands.items():
        name = name.split(";")
        if command == "rename_seqname":
            try: 
                index = Utils.get_index_in_list(name[0], data)
                seq = data[index][-1]
                data_renamed.pop(index)
                data_renamed.insert(index, [name[1], seq])
            except: #print(name[0] + "has not been found in " + filename)
                    print()
    
    return data_renamed

def replace_in_seqname(commands: dict, data: list) -> list:
    """
    Replacing substrings in sequence names in data list by command.

    :param Dictionary commands: All replace_in commands and the corresponding text
    :param List data: List of sequence names and the corresponding sequences

    :return data_replaced: Modified data list with specifically replaced substrings in sequence names
    """
    data_replaced = []
    for name, seq in data:
        for sub_str in commands.keys():
            sub_ls = sub_str.split(";")
            old = sub_ls[0]
            new = sub_ls[1]
            if old in name:
                name = name.replace(old, new)

        data_replaced.append([name, seq])

    return data_replaced


def trim_seqname(commands: list, data: list) -> list:
    """
    Trimming sequence names in data list by command.
    Either trimming after or before a specific character...
    ... or a specific length of characters from the start or the end of the name.

    :param Dictionary commands: All trim commands and the corresponding text
    :param List data: List of sequence names and the corresponding sequences

    :return trimmed_data: Modified data list with specifically trimmed sequence names
    """
    trimmed_data = []
    print(commands)
    for name,seq in data:
        for x,command in commands:
            if command == "trimseqname_after":
                try: name = name[:name.index(x)]
                except: None
            elif command == "trimseqname_before":
                try: name = name[name.index(x)+1:]
                except: None
            elif command == "trimseqname_afterincl":
                try: name = name[:name.index(x)+1]
                except: None
            elif command == "trimseqname_beforeincl":
                try: name = name[name.index(x):]
                except: None
            elif command == "trimseqname_nlastchars":
                try: name = name[-int(x):]
                except: None
            elif command == "trimseqname_nfirstchars":
                try: name = name[:int(x)]
                except: None

        trimmed_data.append([name,seq])

    return trimmed_data

def __Main__(args):

    if type(args) == str:
        args = args.split(" ")
    
    dir_path = args[args.index("--dir") +1]

    all_files_temp = glob.glob(dir_path + "/*")
    all_files = [x for x in all_files_temp if not ".txt" in x and os.path.isfile(x)]

    txt_file = glob.glob(dir_path + "/*.txt")
    commands_temp = read_command_file(txt_file[0])
    commands_rem, extr_commands, commands_ren, commands_repin, commands_trim = commands_processing(commands_temp)

    for file in all_files:
        filename = os.path.basename(file)
        data = Utils.load_fasta_ali_file(file)
        data_removed = remove_seq(commands_rem, data)
        data_renamed = rename_seq(commands_ren, data_removed)
        data_replaced = replace_in_seqname(commands_repin, data_renamed)
        data_trimmed = trim_seqname(commands_trim, data_replaced)
        if ".ali" in filename:
            Utils.write_decont_output(dir_path, filename, data_trimmed, type="protein")
        else:
            Utils.write_decont_output(dir_path, filename, data_trimmed, type="nuclotide")
        
        if extr_commands:
            data_extracted = extract_seq(extr_commands, data)
            if ".ali" in filename:
                Utils.write_decont_output(dir_path, filename, data_extracted, type="protein", folder = "extracted_seqs")
            else:
                Utils.write_decont_output(dir_path, filename, data_extracted, type="nuclotide", folder = "extracted_seqs")

if not sys.argv:
    print("")

elif "--dir" in sys.argv:
    __Main__(sys.argv)

else:
    print(__usage__)
