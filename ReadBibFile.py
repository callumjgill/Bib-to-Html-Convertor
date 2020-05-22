"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/05/20

Description: Takes a .bib file as input and stores the relevant information
"""
# EXTERNAL MODULES
import os
import configparser

# Read the config file
config_parser = configparser.RawConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.properties")
config_parser.read(config_path)

# FUNCTIONS
def readBibEntries(bib_file):
    """
        Function which takes a .bib file input and returns a list of strings where each
        string corresponds to an entry in the file.

        Parameters:
            file : file object
                the .bib file being read. Must be a .bib file otherwise an AssertError exception is made
    """
    ext = bib_file.name.rpartition(".")[-1]
    assert ext == "bib", r"%s is not a .bib file!" % bib_file.name # Call an AssertError if file isn't a .bib file
    contents = bib_file.read() # Contents of the .bib file
    ref_list = contents.split("@") # Creates a list of each entry in the .bib file
    del ref_list[0] # First item in list is blank due to the .split function
    return ref_list

def readEntry(bib_entry):
    """
    Reads the .bib entry and returns a tuple for the entries

    Parameters:
            bib_entry : string
                the entry in the .bib file which has been stored as a string
    """
    # Seperate the entry into entry type and fields
    temp_list = bib_entry.split(",", 1)
    entry_type = temp_list[0]
    fields_list = temp_list[1]
    # Format the entry type string to just be the entry type name
    entry_type = entry_type.split("{", 1)[0]
    

# PUBLIC CLASSES
class reference:
    "Class corresponding to an entry in a .bib file"


    def __init__(self, bib_entry):
        """
        Constructor for reference object. Assigns all fields in .bib entry into
        class attributes

        parameters:
            bib_entry : string
                the entry in the .bib file which has been stored as a string

        """
        #self.entry_type =

# TESTING
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_parser.get("Directory Paths", "bib_path"), "reference.bib")
bib_file = open(filename, "r")
entries = readBibEntries(bib_file)
readEntry(entries[0])