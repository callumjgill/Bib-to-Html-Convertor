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

# Read the config file
CONFIG_PARSER = configparser.RawConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.properties")
CONFIG_PARSER.read(config_path)
# .bib file path name
BIB_PATH = CONFIG_PARSER.get("Directory Paths", "bib_path") + "reference.bib"
# All valid entry and field types from config file
VALID_ENTRIES = dict(CONFIG_PARSER.items("Bib Entry Types"))
VALID_FIELDS = dict(CONFIG_PARSER.items("Bib Field Types"))