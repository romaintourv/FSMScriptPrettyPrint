import os
from FSM import *

directory = "C:\\Users\\Romain\\OneDrive\\Documents\\Trinity Western\\5th Year\\Thesis (CMPT 410)"

cleanFolder = "Clean"

cleanDocx = "List of States"
cleanScripts = "Clean Scripts"

# Path 
cleanFolderPath = os.path.join(directory, cleanFolder)

cleanDocxPath = os.path.join(cleanFolderPath, cleanDocx)
cleanScriptsPath = os.path.join(cleanFolderPath, cleanScripts)

# Create the directory
# 'testFolder' in 
# '/home / User / Documents' 
os.mkdir(cleanFolderPath)

os.mkdir(cleanDocxPath)
os.mkdir(cleanScriptsPath)

# iterate over files in
# that directory
for filename in os.listdir(directory):
    if filename.endswith('.py'):
        fsm = FSM(filename)
        fsm.fixFile()

        newFileName = filename.split(".")

        cleanFilename = newFileName[0] + " clean." + newFileName[1]
        cleanWordDoc = newFileName[0] + " clean list of states.docx"

        os.rename(os.path.join(directory, cleanFilename), os.path.join(cleanScriptsPath, cleanFilename))
        os.rename(os.path.join(directory, cleanWordDoc), os.path.join(cleanDocxPath, cleanWordDoc))
