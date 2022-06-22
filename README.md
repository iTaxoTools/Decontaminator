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
