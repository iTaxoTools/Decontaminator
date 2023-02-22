# decontamination branches
Searching for branches in tree that exceed a certain length 
and deleting all sequences in corresponding .ali and .fasta files that are descendants from this branch.
Also able to delete respective branches from tree.

## Preparing files
Input directory should contain .tre files and corresponding .ali and/or fasta files.
.tre files and corresponding .ali and/or .fasta files should be named similar.

## Running script

```python3 decontamination_branches.py --dir <Path to input directory> --mode <String> --target <String>```

`--mode` Defines if internal branches ('internal') or terminal branches ('terminal') are analyzed.

`--target` Defines what type of file should be decontaminated. Selection between 'alignment', 'tree' or 'both'.

### Additional arguments:

`--perc` Outputs a defined percentage (between 0.0 and 1.0) of longest branches and deletes them from target. --perc <Float>

`--absolute` Outputs a defined number of longest branches and deletes them from target. --absolute <Integer>

`--quantile` Outputs a number of branches that are longer than the critical value of the defined quantile (between 0.0 and 1.0) and deletes them from target. --quantile <Float>

`--factor` Outputs a number of branches that are longer by a given factor than the mean length of their sister species and deletes them from target. --factor <Integer>

`--referencetree` Outputs a number of branches that are longer by a factor than their counter part in the reference tree and deletes them from target. --referencetree <Path to reference .tre file>
 
 ### Logging
 All processes and deleted branches are logged in a log.txt! Please check the log file after each run for Problems that might occur.

# remove-rename
Deleting sequences and renaming sequence names from .ali und .fasta files

## Preparing files
Input directory should contain all necessary .fasta and .ali files 
and one .log/.txt file containing all commands.

## Commands in .log/.txt file

Remove a sequence based on its sequence name
`remove_seq <"Seqname">;`

Rename a sequence
`rename_seqname <"old Seqname"> <"new Seqname">; `

Replace a string of characters within sequence names
`replacein_seqname <"old Substring"> <"new Substring">; `

Trim part of sequence names that follows a specific character (the character will also be deleted)
`trimseqname_after <"Character">; `

Trim part of sequence names that precedes a specific character (the character will also be deleted)
`trimseqname_before <"Character">; `

Trim part of sequence names that follows a specific character (the character will not be deleted)
`trimseqname_afterincl <"Character">;`

Trim part of sequence names that precedes a specific character (the character will not be deleted)
`trimseqname_beforeincl <"Character">; `

Delete a specified number of characters at the end of each sequence name
`trimseqname_nlastchars <Integer>;`

Delete a specified number of characters at the start of each sequence name
`trimseqname_nfirstchars <Integer>;`

### Extract Sequences

You can extract sequences by using the `extract_seq <"Seqname">;` command.
This command is handled outside of the other commands and creates an additional folder where all files with extracted sequences can be found.</br>
!These extracted sequences are not affected by any other commands that might fit to these sequences!

## Running script

```python3 remove_rename.py --dir <Path to input directory>```

# Decontaminator
Deleting sequences from .ali files

## Preparing files
All .ali and .log files from previous step should be in one directory (folder). This input directory should contain an equal amount of .ali and .log files.
The corresponding .ali and .log file should have identical filenames except for the extensions. The modified (decontaminated) .ali files will be written into a new directory.

## Commands in .log/.txt file

Remove a sequence based on its sequence name
`remove_seq <"Seqname">`

Extract a sequence based on its sequence name
`extract_seq <"Seqname">`

## Running the script

1. Through command line: 

```python3 decontamination.py --dir <Path to input directory>```
 
2. Through GUI:

```python3 decontamination_GUI.py```

# Lengthdecont
Deleting sequences that have too much noninformation data.

## Running the script

1. Through command line:
```python3 lengthdecont.py --dir <Path to input directory> --thresh <FLOAT> --mode <STRING_'percentage'_OR_'absolute'> --type <STRING_'protein'_OR_'nucleotide'>```
