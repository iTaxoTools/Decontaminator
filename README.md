# decontamination branches
Searching for branches in tree that exceed a certain length 
and deleting all sequences in corresponding .ali and .fasta files that are descendants from this branch.

## Preparing files
Input directory should contain .tre files and corresponding .ali and/or fasta files.
.tre files and corresponding .ali and/or .fasta files should be named similar.

## Running script

```python3 decontamination_branches.py --dir <Path to input directory> --thresh <Float Threshhold> --mode <String Mode> ```

`--thresh` Defines threshhold above which a branchlength is considered to be too large.

`--mode` Defines if internal branches ('internal') or terminal branches ('terminal') are analyzed.

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
This command is handled outside of the other commands and creates an additional folder where all files with extracted sequences can be found.

!These extracted sequences are not affected by any other commands that might fit to these sequences!

## Running script

```python3 remove_rename.py --dir <Path to input directory>```

# Decontaminator
Deleting sequences from .ali files

## Preparing files
All .ali and .log files from previous step should be in one directory (folder). This input directory should contain an equal amount of .ali and .log files.
The corresponding .ali and .log file should have identical filenames except for the extensions. The modified (decontaminated) .ali files will be written into a new directory.

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
