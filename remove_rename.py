#### rename_seq #####
import Utils
import glob
import os

__usage__ = """
        python3 remove_rename.py
        --dir <PATH_TO_INPUT_FOLDER>
"""


def read_command_file(file):
    commands = {}
    with open(file, "r") as f:
        line = f.readline()

        while line:
            if not line == "\n":
                parts = line.strip().split(" ")
                command = parts[0]
                name = " ".join(parts[1:])
                commands[name] = command
            
            line = f.readline()


    return commands

def commands_processing(commands):
    rem_commands = {}
    ren_commands = {}
    repin_commands = {}
    trim_commands = {}
    for name,command in commands.items():
        if command == "remove_seq":
            s_name = name.replace('"',"")[:-1]
            rem_commands[s_name] = command
        
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
            trim_commands[name] = command

    return rem_commands, ren_commands, repin_commands

def remove_seq(commands, data):
    data_removed = data.copy()
    for name,command in commands.items():
         if command =="remove_seq":
            try: 
                index = Utils.get_index_in_list(name, data)
                data_removed.pop(index)

            except: #print(name + "has not been found in " + filename)
                    print()

    return data_removed

def rename_seq(commands, data):
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

def replace_in_seqname(commands, data):
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


def trim_seqname(commands, data):
    trimmed_data = []
    for name,seq in data:
        for x,command in commands.items():
            if command == "trimseqname_after":
                name = name[:name.index(x)]
            elif command == "trimseqname_before":
                name = name[name.index(x)+1:]
            elif command == "trimseqname_afterincl":
                name = name[:name.index(x)+1]
            elif command == "trimseqname_beforeincl":
                name = name[name.index(x):]
            elif command == "trimseqname_nlastchars":
                name = name[-x:]
            elif command == "trimseqname_nfirstchars":
                name = name[:x]

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
    commands_rem, commands_ren, commands_repin = commands_processing(commands_temp)

    for file in all_files:
        filename = os.path.basename(file)
        data = Utils.load_fasta_ali_file(file)
        data_removed = remove_seq(commands_rem, data)
        data_renamed = rename_seq(commands_ren, data_removed)
        data_replaced = replace_in_seqname(commands_repin, data_renamed)
        data_trimmed = trim_seqname(commands_repin, data_replaced)
        if ".ali" in filename:
            Utils.write_decont_output(dir_path, filename, data_trimmed, type="protein")
        else:
            Utils.write_decont_output(dir_path, filename, data_trimmed, type="nuclotide")
    

if not sys.argv:
    print("")

elif "--dir" in sys.argv:
    __Main__(sys.argv)

else:
    print(__Usage__)
