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

# CLASSES

class HTMLCite:
    "Class which stores the contents of a .bib reference to be processed into readable HTML code"

    # CONSTRUCTOR
    def __init__(self, bib_reference):
        """
            Constructor

            Parameters:
                bib_reference: Reference class
                    Meta-information on a reference is stored in this class.
            
            Returns:
                None
        """
        self.entry_type = bib_reference.entry_type # String
        self.fields = bib_reference.fields # Dictionary
        self.__format2Html() # Calls method to process the entries and appropriatly format the content
    
    def __format2Html(self):
        """
            Formats the content of specific fields in each entry in the .bib file into readable HTML code

            Parameters:
                None
            
            Returns:
                None
        """
        # Processes all fields which must be in an italic font
        if self.entry_type in ITALIC_FIELDS:
            for field, content in self.fields.items():
                if field in ITALIC_FIELDS[self.entry_type]:
                    self.fields[field] = "<i>" + content + "</i>" # Converts to italic HTML code
        # Joins each individual author into a single string seperated by commas
        if "author" in self.fields:
            self.fields["author"] = ", ".join(self.fields["author"])
        if self.entry_type == "article":
            # The field "number" is always written inside parenthesis when an entry type is an article
            if "number" in self.fields:
                self.fields["number"] = "(" + self.fields["number"] + "):" # Adds parenthesis around the number field type
        else:
            # When the entry isn't an article the page numbers are written following the word "pages"
            if "pages" in self.fields:
                self.fields["pages"] = "pages " + self.fields["pages"]
            # If the entry is an article then editor won't be processed as a field type
            if "editor" in self.fields:
                self.fields["editor"] = ", ".join(self.fields["editor"]) + ", editors"
            if "booktitle" in self.fields:
                self.fields["booktitle"] = "In " + self.fields["booktitle"]
            # Deals with the /url{} in howpublished
            if "howpublished" in self.fields:
                self.fields["howpublished"] = self.fields["howpublished"][3:] #removes url from first part of string

# FUNCTIONS                  
# Write references into a .html file
def convert2Html(references):
    """
        Converts all of the references in the .bib file into a readable HTML code file.
        References are written as an ordered list in HTML in the order they appear in the .bib file.

        Parameters:
            references: list of HTMLCite classes

        Returns:
            None
    """
    # Base code for each file
    start = "<html><body><ol>"
    end = "</ol></body></html>"
    # Stores the full HTML code as a string to be written to a .html file
    html_code = "" # Start as empty string
    # Iterate over every reference in the list
    for ref in references:
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
        html_code += "<li>" + ref_html + "</li>"
    html_code = start + html_code + end # Final html code
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ReadConfig.HTML_PATH)
    with open(file_path + "references.html", "w+") as html_file:
        html_file.write(html_code)
    


# TESTING
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), ReadConfig.BIB_PATH)
bib_file = open(filename, "r")
references = [HTMLCite(ref) for ref in BibParser.bibParser(bib_file)]
bib_file.close()
convert2Html(references)