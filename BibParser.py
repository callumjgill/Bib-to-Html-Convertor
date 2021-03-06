"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/05/20

Description: Parser that takes a .bib file as input and stores the each entry as an 
object with the fields being the objects attributes and are stored as dictionaries .
"""
# MODULES
import os
import ReadConfig
import collections

# GLOBAL VARIABLES
VALID_ENTRIES = ReadConfig.getSectionItems("Bib Entry Types")
VALID_FIELDS = ReadConfig.getSectionItems("Bib Field Types")
REQUIRED_FIELDS = ReadConfig.getSectionItems("Required Fields")
OPTIONAL_FIELDS = ReadConfig.getSectionItems("Optional Fields")
# Message global variable for error
MSG_FILE = "" # Filename is assigned in bibParser

# FUNCTIONS
def bibParser(bib_file):
    """
        Takes a .bib filename input and returns an list of Reference objects where each
        object corresponds to an entry in the file. List is ordered in the order in which each
        entry appears in the .bib file, not the document or order the references appear in.

        Parameters:
            bib_file : file object
                the .bib file being read. Must be a .bib file otherwise an AssertError exception is made

        Returns:
            ref_list : list of Reference objects
                each item in the list is an object corresponding to a single reference 
                entry in the .bib file and 
    """
    global MSG_FILE
    ext = bib_file.name.rpartition(".")[-1]
    if ext != "bib":
        raise ValueError(r"%s is not a .bib file!" % bib_file.name) # Raise a ValueError if file isn't a .bib file
    MSG_FILE += bib_file.name
    contents = bib_file.read() # Contents of the .bib file
    ref_list_str = contents.split("@") # Creates a list of each entry in the .bib file
    del ref_list_str[0] # First item in list is blank due to the .split function
    ref_list = [Reference(ref) for ref in ref_list_str]
    return ref_list

# CLASSES
class Reference:
    "Class corresponding to an entry in a .bib file"

    # CONSTRUCTOR

    def __init__(self, bib_entry):
        """
            Constructor for reference object. Assigns all fields in .bib entry into
            class attributes

            parameters:

                bib_entry : string
                    the entry in the .bib file which has been stored as a string
            
            Returns:
                None
        """
        self.entry_type, self.fields = self.__readEntry(bib_entry)

    # METHODS
    ## "PRIVATE"
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
        # Format the entry type string to just be the entry type name and the other side of the { char is the entry name
        entry_type, entry_name = entry_type.split("{", 1)
        if not self.__checkIfValid(entry_type, VALID_ENTRIES):
            err_msg = entry_type + " is not a valid entry type!\n" + "Entry: " + entry_name + "\nFile: " + MSG_FILE
            raise ValueError(err_msg)
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
            if not self.__checkIfValid(key, VALID_FIELDS):
                err_msg = key + " is not a valid field type!\n" + "Entry: " + entry_name + "\nFile: " + MSG_FILE
                raise ValueError(err_msg)
            # checks if the field type can actually be used with the entry type
            if not self.__checkField(entry_type, key):
                err_msg = key + " isn't a recognised field type for the entry type " + entry_type + "!\nEntry: " + entry_name + "\nFile: " + MSG_FILE
                raise ValueError(err_msg)
            # Removes unnecessary characters from the value
            value = key_value_list[1].replace("{", "").replace("}", "").replace(' "', "").replace('"', "").replace(" \\", "")
            # If the field type is author or editor then each author/editor is stored as a list of strings
            if key == 'author' or key == 'editor':
                # Splits string at the comma for each author.
                value = value.replace(", ", ",").split(",")
                # Removes whitespace in front of each author name if there is any
                for index, item in enumerate(value):
                    if item[0] == " ":
                        item.replace(" ", "", 1)
                        value[index] = item
            elif key == "howpublished":
                # Deals with the possibility of a /url{} in howpublished if present
                if value[:3] == "url":
                    value = value[3:] #removes url from first part of string
            # Builds the dictionary with each field entry type as a key and the value the content of the field
            fields[key] = value
        # Final check is to see if all required fields have been given
        if entry_type != "misc":
            required_fields_given = [item for item in fields if item in REQUIRED_FIELDS[entry_type]]
            if collections.Counter(required_fields_given) != collections.Counter(REQUIRED_FIELDS[entry_type]):
                missing_msg = r"Missing required fields!\n Fields given: %s \n Fields required: %s \n" % (", ".join(fields.keys()), ", ".join(REQUIRED_FIELDS[entry_type]))
                err_msg = repr(missing_msg).replace("\\n", "\n") + "Entry: " + entry_name + "\nFile: " + MSG_FILE + "\nLines: "
                raise ValueError(repr(missing_msg).replace("\\n", "\n"))
        return (entry_type, fields)

    def __checkField(self, entry_type, field):
        """
            Checks if the field is a required or optional for the entry_type.
            Returns True if its required or optional. If not it returns False.

            Parameters:
                entry_type : string
                    The corresponding entry type of the field being tested
                field : string
                    The field being tested.
            
            Returns:
                is_valid : boolean
                    True if valid, False otherwise
        """
        is_valid = False
        # required fields for the entry type
        required = REQUIRED_FIELDS[entry_type]
        # optional fields for the entry type
        optional = OPTIONAL_FIELDS[entry_type]
        if field in required or field in optional:
            is_valid = True
        return is_valid

    def __checkIfValid(self, input_test, config_section):
        """
            Checks if the input (field or entry type) appears in the config file
            and returns True if so, otherwise False.

            Parameters:
                input_test : string
                    The input being tested

                config_section : dictionary
                    The dictionary that the input is being tested against

            Returns:
                in_config : boolean
                    True if valid, False otherwise
        """
        in_config= False
        if input_test in config_section.keys():
            in_config = True
        return in_config