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

Entferne Sequenz anhand Sequenzname
``` remove_seq <"Seqname">; ```

Umbennenen des Sequenznamens
```rename_seq <"old Seqname"> <"new Seqname">; ```

Ersetzen eines Strings innerhalb eines Sequenznamens
```replacein_seqname <"old Substring"> <"new Substring">; ```

Löschen des Sequenznamens hinter bestimmtem Zeichen (Zeichen wird mit gelöscht)
```trimseqname_after <"Character">; ```

Löschen des Sequenznamens vor bestimmtem Zeichen (Zeichen wird mit gelöscht)
```trimseqname_before <"Character">; ```

Löschen des Sequenznamens vor bestimmtem Zeichen (Zeichen wird nicht gelöscht)
```trimseqname_afterincl <"Character">;```

Löschen des Sequenznamens vor bestimmtem Zeichen (Zeichen wird nicht gelöscht)
```trimseqname_beforeincl <"Character">; ```

Löschen der Anzahl Zeichen am Ende des Sequenznamens
```trimseqname_nlastchars <Integer>;```

Löschen der Anzahl Zeichen am Anfang des Sequenznamens
```trimseqname_nfirstchars <Integer>;```

## Running script

```python3 remove_rename.py --dir <Path to input directory>```

# Decontaminator
Deleting sequences from .ali files

## Preparing files
Input direcotry should contain equal amount of .ali and .log files.
Corresponding .ali and .log file should be named the same.

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
