"""
Author: Callum J Gill.
Email: callum.j.gill@googlemail.com
Date created: 21/07/20

Description: Runs the entirety of the app via a PyQt5 GUI.
"""

import sys
import os
import ReadConfig
import BibParser
import ConvertToHtml
from PyQt5.QtCore import QFileInfo, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        """
            Constructor for the GUI.

            Parameters:
                None
            
            Returns:
                None 
        """
        super().__init__()
        self.title = "Bib to HTML convertor"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 280
        self.initUI()

    def initUI(self):
        """
            Method to initalise the GUI widgets.

            Parameters:
                None
            
            Returns:
                None 
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # File Load and Saving
        # Buttons for choosing .bib file and directory for saving the .html file
        # Textbox shows the loaded filepath

        self.bib_file_name = "" # Bib file path
        self.loadTxtBox = QLineEdit(self)
        self.loadTxtBox.setReadOnly(True) # Ensures the textbox is uneditable
        self.loadTxtBox.move(240, 75)
        self.loadTxtBox.resize(300, 20)

        self.loadButton = QPushButton("Load .bib file", self)
        self.loadButton.setToolTip("Choose the .bib file to convert")
        self.loadButton.move(100, 70)
        self.loadButton.clicked.connect(self.onClickLoad)

        self.html_file_name = "" # Bib file path
        self.saveTxtBox = QLineEdit(self)
        self.saveTxtBox.setReadOnly(True) # Ensures the textbox is uneditable
        self.saveTxtBox.move(240, 105)
        self.saveTxtBox.resize(300, 20)

        self.saveButton = QPushButton("Save .html file", self)
        self.saveButton.setToolTip("Choose the filepath to save the .html file to")
        self.saveButton.move(100, 100)
        self.saveButton.clicked.connect(self.onClickSave)

        # Button to convert the bib file to html
        self.convertButton = QPushButton("Convert file", self)
        self.convertButton.setToolTip("Convert the chosen .bib file to a .html file with the chosen filepath")
        self.convertButton.move(250, 150)
        self.convertButton.clicked.connect(self.onClickConvert)

        self.show()
    
    @pyqtSlot()
    def onClickLoad(self):
        """
            Method executed when the load .bib file button is pressed.
            Returns the filepath name and displays it in the adjacent textbox.

            Parameters:
                None
            
            Returns:
                None 
        """
        self.bib_file_name = self.openFileNameDialog()
        self.loadTxtBox.setText(self.bib_file_name)


    @pyqtSlot()
    def onClickSave(self):
        """
            Method executed when the save .html file button is pressed.
            Returns the filepath name and displays it in the adjacent textbox.

            Parameters:
                None
            
            Returns:
                None 
        """
        self.html_file_name = self.saveFileDialog()
        self.saveTxtBox.setText(self.html_file_name)

    @pyqtSlot()
    def onClickConvert(self):
        """
            Method executed when the convert file button is pressed.
            Executes the code given in ReadConfig.py, BibParser.py and ConvertToHtml.py,
            which converts the specified .bib file to a .html file with the given pathname

            Parameters:
                None
            
            Returns:
                None 
        """
        # Checks if the bib and html file path names are empty, if both arent then execute the main code.
        if self.bib_file_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Please select a bib file to convert!")
            msg.setWindowTitle("No bib file to convert!")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()
        elif self.html_file_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Please choose a pathname to save the html file to!")
            msg.setWindowTitle("No html pathname!")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()
        else:
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.bib_file_name)
            with open(filename, "r") as bib_file:
                try:
                    references = [ConvertToHtml.format2Html(ref) for ref in BibParser.bibParser(bib_file)]
                    ConvertToHtml.convert2Html(references, self.html_file_name)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)

                    msg.setText("Conversion succesfully complete!")
                    msg.setWindowTitle("Sucessful conversion")
                    msg.setStandardButtons(QMessageBox.Ok)

                    msg.exec_()
                    self.saveTxtBox.setText("")
                    self.loadTxtBox.setText("")

                except ValueError as message:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)

                    msg.setText("An error occured during the conversion!")
                    msg.setWindowTitle("Error!")
                    msg.setDetailedText(str(message))
                    msg.setStandardButtons(QMessageBox.Ok)

                    msg.exec_()
        

    def openFileNameDialog(self):
        file_name = QFileDialog.getOpenFileName(self, self.tr("Load bib document"), "", self.tr("bib files (*.bib)"))[0]
        if file_name:
            if not QFileInfo(file_name).suffix():
                file_name += ".bib"
        return file_name
    
    def saveFileDialog(self):
        file_name = QFileDialog.getSaveFileName(self, self.tr("Save html file"),"",self.tr("html files (*.html)"))[0]
        if file_name:
            if not QFileInfo(file_name).suffix():
                file_name += ".html"
        return file_name

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())