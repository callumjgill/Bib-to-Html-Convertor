"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/05/20

Description: Takes a .bib file as input and stores the relevant information
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
    ref_list = contents.split("@") # Creates a list of each entry in the .bib file
    del ref_list[0] # First item in list is blank due to the .split function
            

filename = BIB_DIR + "reference.bib"
bib_file = open(filename, "r")
readBib(bib_file)