# FSMScriptPrettyPrint

This repository contains Python scripts for correcting spacing issues in Python scripts that do not follow Python conventions.

## Finite State Machine (FSM.py)

`FSM.py` is a finite state machine (FSM) implementation that corrects spacing issues in Python scripts. It analyzes the input Python script and corrects indentation, spacing, and formatting inconsistencies to adhere to Python conventions.

## Mongoose.py

`Mongoose.py` implements the FSM to correct a single file of your choice. Just change "your_file_here.py" to the file of your choice. The output will be two files: a clean Python file and a .docx file containing all states the FSM went through. Your original file will not be changed.

## Mongooses.py

`Mongooses.py` corrects an entire folder. It will only correct Python scripts. The output will be a "Clean" folder in that directory. In it will be two folders: "List of states" folder for all .docx files and "Clean scripts" folder for all clean scripts. The names of all of these files will follow the same naming pattern as the resulting files from Mongoose.py. Note: an extra "\" should be added to each "\" in the directory path as "\" is an escape character in Python.

# test.py

`test.py` is an example file for you to test `FSM.py` if you are unsure. Feel free to change `test.py` to see what the FSM can do.
