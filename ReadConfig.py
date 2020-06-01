"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 30/05/20

Description: Reads all the sections in config.properties 
and stores them as global variables that are imported into the other .py files
"""
# MODULES
import os
import configparser

# GLOBAL VARIABLES
CONFIG_PARSER = configparser.RawConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.properties")
CONFIG_PARSER.read(config_path)
# .bib file path name
BIB_PATH = CONFIG_PARSER.get("Directory Paths", "bib_path") + "reference.bib"

def getSectionItems(section_name):
    """
        Returns a dictionary containing every item in a section of the config.properties file.

        Parameters:
            section_name : section_name
                the name of the section to retrieve the items from

        Returns:
            dict_of_items : dictionary {key:value}
                dictionary corresponds to each key:value pair in the config.properties file
    """
    list_of_items = CONFIG_PARSER.items(section_name)
    dict_of_items = {}
    if section_name == "Bib Entry Types" or section_name == "Bib Field Types":
        # Items which are set to true in config.properties are only returned
        dict_of_items = dict([item for item in list_of_items if item[1].lower() == 'true'])
    else:
        # If the value in config.properties is a list, where each list item is separated by a comma,
        # then store the value as a list in the dictionary
        # Seperate a value representing a list into an actual list and remove whitespace
        dict_of_items = dict([(key, value.replace(" ", "").split(",")) for (key, value) in list_of_items])
    return dict_of_items