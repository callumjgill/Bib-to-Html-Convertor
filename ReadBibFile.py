"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/05/20
Date modified: 21/05/20

Description: Takes a .bib file as input and reads the relevant information
"""
# EXTERNAL MODULES
import os

# GLOBAL VARIABLES
BIB_DIR = r"test-bib-files/" # Folder to read the bib files from
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BIB_DIR = os.path.join(CURRENT_DIR, BIB_DIR)

# PUBLIC FUNCTIONS
def readBib(bib_file):
    """
        Function which takes a .bib file input and returns a list of dictionaries where each
        dictionary corresponds to an entry in the file.

        Parameters:
            file : file object
                the .bib file being read. Must be a .bib file otherwise an AssertError exception is made
    """
    ext = bib_file.name.rpartition(".")[-1]
    assert ext == "bib", r"%s is not a .bib file!" % bib_file.name # Call an AssertError if file isn't a .bib file
    contents = bib_file.read() # Contents of the .bib file
    # Find all the indexes for each @ char in the .bib file i.e. find the start of each reference
    ref_indexes = [i for i, char in enumerate(contents) if char == "@"] # All indexes of the start of each reference in the file
    ref_indexes.append(-1) # Prevents an IndexError occuring in the list when the final entry is reached
    ref_list = []
    for i, index in enumerate(ref_indexes):
        next_index = ref_indexes[i+1]
        if next_index == -1:
            ref_list.append(contents[index:])
            break # break the loop once the last entry is read and stored
        ref_list.append(contents[index:next_index])
    
            

filename = BIB_DIR + "reference.bib"
bib_file = open(filename, "r")
readBib(bib_file)