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
CONFIG_PARSER = configparser.RawConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.properties")
CONFIG_PARSER.read(config_path)
# All valid entry and field types from config file
VALID_ENTRIES = dict(CONFIG_PARSER.items("Bib Entry Types"))
VALID_FIELDS = dict(CONFIG_PARSER.items("Bib Field Types"))

# FUNCTIONS
def readBibEntries(bib_file):
    """
        Function which takes a .bib file input and returns a list of strings where each
        string corresponds to an entry in the file.

        Parameters:
            file : file object
                the .bib file being read. Must be a .bib file otherwise an AssertError exception is made

        Returns:
            ref_list : list of strings
                each item in the list is an object corresponding to a single reference entry in the .bib file
    """
    ext = bib_file.name.rpartition(".")[-1]
    assert ext == "bib", r"%s is not a .bib file!" % bib_file.name # Call an AssertError if file isn't a .bib file
    contents = bib_file.read() # Contents of the .bib file
    ref_list_str = contents.split("@") # Creates a list of each entry in the .bib file
    del ref_list_str[0] # First item in list is blank due to the .split function
    ref_list = [Reference(ref) for ref in ref_list_str]
    return ref_list

# PUBLIC CLASSES
class Reference:
    "Class corresponding to an entry in a .bib file"


    def __init__(self, bib_entry):
        """
            Constructor for reference object. Assigns all fields in .bib entry into
            class attributes

            parameters:
                bib_entry : string
                    the entry in the .bib file which has been stored as a string

        """
        self.entry_type, self.fields = self.__readEntry(bib_entry)

    # "PRIVATE" METHODS
    def __readEntry(self, bib_entry):
        """
            Reads the .bib entry and returns a tuple with the entry type as a string and a
            dictionary for the fields.

            Parameters:
                    bib_entry : string
                        the entry in the .bib file which has been stored as a string

            Returns:
                (entry_type, fields) : (string, dictionary)
                    the entry type is stored as a string. The keys in the dictionary 
                    are the field types and the corresponding values are the content
        """
        # Seperate the entry into entry type and fields
        temp_list = bib_entry.split(",", 1)
        entry_type = temp_list[0]
        fields_list_str = temp_list[1].replace("\n", "").replace("\t", "") # single string storing all fields, also replaces irrelevant characters
        # Format the entry type string to just be the entry type name
        entry_type = entry_type.split("{", 1)[0]
        assert self.__checkEntry(entry_type), r"%s is not a valid entry type!" % entry_type
        # Format the fields into a list and then into a dictionary
        # First it replaces the string '},' whereever it appears with '",'
        # Then it splits at '",". This will then correctly get each field entry as you can either enclose them in " " or { }
        fields_list = fields_list_str.replace('},', '",').split('",')
        fields = {}
        # Now the field name and content is split up
        for field in fields_list:
            key_value_list = field.split("=")
            key = key_value_list[0].replace(" ", "")
            # checks if the field type is valid
            assert self.__checkField(key), r"%s is not a valid field type!" % key
            # Removes unnecessary characters from the value
            value = key_value_list[1].replace("{", "").replace("}", "").replace(' "', "").replace('"', "")
            # If the field type is author then each author is stored as a list of strings
            if key == 'author':
                # Removes whitespace in front of first author name and splits string a the comma. Also removes whitespace in front of other authors if there is any
                value = value.replace(" ", "", 1).replace(", ", ",").split(",")
            # Builds the dictionary with each field entry type as a key and the value the content of the field
            fields[key] = value
        return (entry_type, fields)

    def __checkEntry(self, entry_type):
        """
            Checks the entry type against the config file for valid entry types.

            Parameters:
                entry_type : string
                    The entry type being tested

            Returns:
                is_valid : boolean
                    true if valid, false otherwise
        """
        is_valid = False
        if entry_type in VALID_ENTRIES.keys():
            is_valid = True
        return is_valid

    def __checkField(self, field):
        """
            Checks the field type against the config file for valid field types.
            
            Parameters:
                field : string
                    The field type being tested

            Returns:
                is_valid : boolean 
                    true if valid, false otherwise
        """
        is_valid = False
        if field in VALID_FIELDS.keys():
            is_valid = True
        return is_valid

# TESTING
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIG_PARSER.get("Directory Paths", "bib_path"), "reference.bib")
bib_file = open(filename, "r")
entries = readBibEntries(bib_file)