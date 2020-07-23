"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/05/20

Description: Takes each reference object handled by ReadBibFile.py 
and processes it into a html file
"""
import os
import ReadConfig
import BibParser

# GLOBAL VARIABLES
ORDER_OF_FIELDS = ReadConfig.getSectionItems("Field Order")
ITALIC_FIELDS = ReadConfig.getSectionItems("Italic Fields")

# FUNCTIONS
def format2Html(ref):
    """
        Formats the content of specific fields in each entry in the .bib file into readable HTML code

        Parameters:
            ref : A BibParser Reference object to format the information from
        
        Returns:
            format_ref : A formatted Reference object
    """
    # Processes all fields which must be in an italic font
    if ref.entry_type in ITALIC_FIELDS:
        for field, content in ref.fields.items():
            if field in ITALIC_FIELDS[ref.entry_type]:
                ref.fields[field] = "<i>" + content + "</i>" # Converts to italic HTML code
    # Joins each individual author into a single string seperated by commas
    if "author" in ref.fields:
        ref.fields["author"] = ", ".join(ref.fields["author"])
    if ref.entry_type == "article":
        # The field "number" is always written inside parenthesis when an entry type is an article
        if "number" in ref.fields:
            ref.fields["number"] = "(" + ref.fields["number"] + "):" # Adds parenthesis around the number field type
    else:
        # When the entry isn't an article the page numbers are written following the word "pages"
        if "pages" in ref.fields:
            ref.fields["pages"] = "pages " + ref.fields["pages"]
        # If the entry is an article then editor won't be processed as a field type
        if "editor" in ref.fields:
            ref.fields["editor"] = ", ".join(ref.fields["editor"]) + ", editors"
        if "booktitle" in ref.fields:
            ref.fields["booktitle"] = "In " + ref.fields["booktitle"]
    return ref
    

# Write references into a .html file
def convert2Html(refs, html_file_name):
    """
        Converts all of the references in the .bib file into a readable HTML code file.
        References are written as an ordered list in HTML in the order they appear in the .bib file.

        Parameters:
            refs: list of Reference classes
                list of Reference classes that have already been formatted from the format2Html() function
            
            html_file_name : string
                filepath to save the html file to

        Returns:
            None
    """
    # Base code for each file
    start = "<html>\n\t<body>\n\t\t<ol>\n"
    end = "\t\t</ol>\n\t</body>\n</html>"
    # Stores the full HTML code as a string to be written to a .html file
    html_code = "" # Start as empty string
    # Iterate over every reference in the list
    for ref in refs:
        ref_html = "" # Stores the html code for the reference in the list
        # Iterate over the dictionary containing the order in which fields are processed to write the entry out
        for field in ORDER_OF_FIELDS[ref.entry_type]:
            if field in ref.fields:
                ref_html += ref.fields[field]
                # Join each fields content by a comma or fullstop
                if field == "author" or field == "title" or field == "pages":
                    ref_html += ". "
                else:
                    ref_html += ", "
        ref_html = ref_html[:-2] + "." # Replaces last comma with a fullstop
        html_code += "\t\t\t<li>" + ref_html + "</li>\n"
    html_code = start + html_code + end # Final html code
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), html_file_name)
    with open(file_path, "w+") as html_file:
        html_file.write(html_code)