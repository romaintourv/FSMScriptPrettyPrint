from docx import Document
class FSM:
    '''States: Start, In Token, Found Space, Found Operator, Need a Space, Too Many Spaces,
    Found Colon, Found Newline, Found Tab, Too Many New Lines, Found Open parentheses,
    Found Close parentheses, Found Comma, End of File
    
    Triggers:

    Need a Space:
        From:                   With:
        In Token                 Any operator
        Found Operator           Any char or numb
        Found Comma              Any char or numb
        Found close parentheses Any char or numb

    "found extra space":
        From:                   With:
        "found extra space"        Space
        Found Tab               Space
        Found Open parenthesess  Space
        Found Space             comma, colon, newline
        Colon                   Space
        found space             !space and (counter % 4 != 0)
    
    Too Many New Lines:
        From:                   With:
        Start                   Newline
        Found Newline           Newline

    In Token:
        From:                   With:
        In Token                Any char or numb
        Start                   Any char or numb
        Found Space             Any char or numb
        Found Newline           Any char or numb
        Found Tab               Any char or numb
        Too Many New Lines      Any char or numb
        "found extra space"        Any char or numb
        Found Open parentheses   Any char or numb
    
    Found Colon:
        From:                   With:
        In Token                Colon
        Found Close Parethese   Colon

    Found Newline 1:
        From:                   With:
        Found Colon             Newline
        In Token                Newline
        in comment              Newline

    Found Newline 2:
        Found newline 1         newline

    Found Space:
        From:                   With:
        Found Space             Space
        In Token                Space
        Need a Space            Space
        found operator             space
    
    Found Operator:
        From:                   With:
        Found Space             Any Operator
        found operator          any operator

    Found Tab:
        From:                   With:
        Found Tab               Tab
        Found Newline           Tab
        Too Many New Lines      Tab

    Found Comma:
        From:                   With:
        In token                Comma

    Found Open parentheses:
        From:                   With:
        In token                Open Paretheses
        Space                   Open Parentheses

    Found Close parentheses:
        From:                   With:
        In token                Close parentheses
        found open parentheses  Close parentheses

    In string:
        From:                   With:

        
    TODO:
    in line extra spaces, unlike tab extra spaces. differentiate those two
    Figure out extra tabs
    '''

    def __init__(self, file) -> None:
        self.file = file
        self.charIndex = 1 # to know where convention is not respected
        self.lineIndex = 1
        self.sequence = ["start"]
        self.state = "start"
        self.currentCharacter = ""
        self.spaceCounter = 0
        self.tokens = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z", ".", "]", "}", "_"]
        self.document = Document()
        self.prevTabLen = 0

        self.newline = True
        # Conditions for transtions between states
        self.toTokenStates = ["start", "in token", "found newline 1", "found newline 2",
            "found extra line", "found extra space", "found open parentheses", "found space"]
        self.toNeedASpaceStates = ["found operator", "found comma", "found close parentheses", "found colon"]

        self.foundXtraSpaceStates = ["found open parentheses", "found extra space"]
        self.foundXtraSpaceChars = [")", ",", ":", '\n', ";", "]", "}"]

        self.foundXtraLineStates = ["start", "found newline 2", "found extra line", "found tab"]

        self.operators = ['+', '-', '*', '/', '%', '=', '>', '<', '!', '&', '|', '^']
        self.openParentheses = ["(", "[", "{"]
        self.closeParentheses = [")", "]", "}"]
        self.separator = [",", ";"]

        self.toFoundNewLineStates = ["found colon", "in token", "in comment", "need a space", "found extra space", "out string", "found comma", "found open parentheses", "found close parentheses"]
        self.toFoundSpaceStates = ["in token", "need a space", "found operator", "found space", "out string", "found colon", "found close parentheses", "found comma"]

        self.toFoundTabStates = ["found newline 1", "found newline 2", "found tab", "found extra line"]

        self.toFoundColonStates = ["found close parentheses", "in token", "found open parentheses", "out string"]
        self.toFoundCloseParenthesesStates = ["in token", "found open parentheses", "out string", "found close parentheses"]
        self.toFoundOpenParenthesesStates = ["in token", "found space", "found open parentheses"]
        self.toFoundOperatorStates = ["found space", "found operator", "need a space", "found open parentheses"]

        self.xtraTabSpace = False
        self.xtraTab = False
    def currentState(self):
        '''
        Get the state the FSM is currently
        '''
        return self.state
    def updateState(self):

        currentChar = self.currentCharacter
        # Update position of FSM
        if currentChar == "\n":
            self.lineIndex += 1
            self.charIndex = 1
            self.newline = True
        elif currentChar != "\n" and currentChar != " " and self.newline == True:
            self.charIndex += 1
            self.newline = False
        else:
            self.charIndex += 1

        # In comment state
        if currentChar == "#" or (self.currentState() == "in comment" and currentChar != "\n"):
            self.state = "in comment"
            self.sequence.append(self.state)
            return
        # in string
        if (self.currentState() == "in string" and (currentChar != '\"' and currentChar != "\'" and currentChar != "\\")) or self.currentState() == "found escape":
            self.state = "in string"
            self.sequence.append(self.state)
            return

        # In token state
        elif currentChar in self.tokens and (self.currentState() in self.toTokenStates or (self.currentState() == "found tab" and self.spaceCounter // 4 <= (self.prevTabLen + 1) and self.spaceCounter % 4 == 0)):
            self.state = "in token"
            self.sequence.append(self.state)
        # Need a space state by token
        elif self.currentState() in self.toNeedASpaceStates and currentChar in self.tokens:
            self.state = "need a space"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)
            self.state = "in token"

        # Need a space state by operator
        elif (self.currentState() == "in token" or self.currentState() == "found close parentheses" or self.currentState() == "out string") and currentChar in self.operators:
            self.state = "need a space"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)
            self.state = "found operator"
        # Need a space state by string
        elif self.currentState() == "found operator" and (currentChar == "\"" or currentChar == "\'"):
            self.state = "need a space"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)
            self.state = "in string"

        # Found extra space state
        elif (self.currentState() in self.foundXtraSpaceStates and currentChar == " ") or (self.currentState() == "found space" and currentChar in self.foundXtraSpaceChars) or (self.currentState() == "found space" and currentChar == " " and self.newline == False):
            self.state = "found extra space"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)

            if currentChar == "\n":
                self.state = "found newline 1"
                self.spaceCounter = 0
            elif currentChar == ":":
                self.state = "found colon"
            elif currentChar in self.separator:
                self.state = "found comma"
            elif currentChar in self.closeParentheses:
                self.state = "found close parentheses"
            elif currentChar in self.tokens:
                self.state = "in token"
            elif currentChar in self.operators:
                self.state = "found operator"
            elif currentChar == " ":
                self.state = "found space"
            elif currentChar == "\"" or currentChar == "\'":
                self.state = "in string"

        # Found extra tab
        elif ((self.currentState() == "found tab" and (currentChar != " " and currentChar != "\n")) and (self.spaceCounter // 4 > (self.prevTabLen + 1) or self.spaceCounter % 4 != 0)):
            self.state = "found extra tab"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)

            if self.spaceCounter // 4 > (self.prevTabLen + 1):
                self.xtraTab = True
            if self.spaceCounter % 4 != 0:
                self.xtraTabSpace = True

            self.spaceCounter = self.prevTabLen * 4

            if currentChar == ":":
                self.state = "found colon"
            elif currentChar in self.separator:
                self.state = "found comma"
            elif currentChar in self.closeParentheses:
                self.state = "found close parentheses"
            elif currentChar in self.openParentheses:
                self.state = "found open parentheses"
            elif currentChar in self.tokens:
                self.state = "in token"
            elif currentChar == "\"" or currentChar == "\'":
                self.state = "in string"

        # Found extra line
        elif self.currentState() in self.foundXtraLineStates and currentChar == "\n":
            self.state = "found extra line"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)
            self.spaceCounter = 0

        # Found operator state
        elif self.currentState() in self.toFoundOperatorStates and currentChar in self.operators:
            self.state = "found operator"
            self.sequence.append(self.state)

        # Found comma state
        elif (self.currentState() == "in token" or self.currentState() == "out string") and currentChar in self.separator:
            self.state = "found comma"
            self.sequence.append(self.state)

        # Found newline 1
        elif (self.currentState() in self.toFoundNewLineStates) and currentChar == "\n":
            self.state = "found newline 1"
            self.sequence.append(self.state)
            self.prevTabLen = self.spaceCounter // 4
            self.spaceCounter = 0

        # Found newline 2
        elif (self.currentState() == "found newline 1") and currentChar == "\n":
            self.state = "found newline 2"
            self.sequence.append(self.state)
        # Found space
        elif self.currentState() in self.toFoundSpaceStates and currentChar == " " and self.newline == False:
            self.state = "found space"
            self.sequence.append(self.state)

        # Found tab
        elif self.currentState() in self.toFoundTabStates and currentChar == " " and self.newline == True:
            self.state = "found tab"
            self.spaceCounter += 1
            self.sequence.append(self.state)

        # Found open parentheses state
        elif self.currentState() in self.toFoundOpenParenthesesStates and currentChar in self.openParentheses:
            self.state = "found open parentheses"
            self.sequence.append(self.state)
        # Found close parentheses state
        elif self.currentState() in self.toFoundCloseParenthesesStates and currentChar in self.closeParentheses:
            self.state = "found close parentheses"
            self.sequence.append(self.state)
        # Found colon state
        elif self.currentState() in self.toFoundColonStates and currentChar == ":":
            self.state = "found colon"
            self.sequence.append(self.state)

        # in string
        elif (currentChar == "\'" or currentChar == '\"') and self.currentState() != "in string":
            self.state = "in string"
            self.sequence.append(self.state)

        # found escape
        elif currentChar == "\\" and self.currentState() == "in string":
            self.state = "found escape"
            self.sequence.append(self.state)
        # out of string
        elif self.currentState() == "in string" and (currentChar == "\'" or currentChar == '\"'):
            self.state = "out string"
            self.sequence.append(self.state)
        else:
            self.state = "********"
            flag = self.state + " " + str(self.lineIndex) + " " + str(self.charIndex)
            self.sequence.append(flag)
            self.sequence.append(self.state)

    def fixFile(self):
        file = open(self.file, "r")
        newFileName = self.file.split(".")
        newFile = open(newFileName[0] + " clean." + newFileName[1], "w")

        charSequence = ""

        while True:
            self.currentCharacter = file.read(1)
            if not self.currentCharacter:
                self.state = "end of file"
                self.sequence.append(self.state)
                break
            self.updateState()

            # adding space to new file
            if self.sequence[- 1][: len("need a space")] == "need a space":
                newFile.write(" " + self.currentCharacter)
            # do not add new line if extra line
            elif self.sequence[- 1][: len("found extra line")] == "found extra line":
                charSequence = ""
            elif self.sequence[- 1] == "found tab" or self.sequence[- 1] == "found space":
                charSequence += self.currentCharacter
            elif self.sequence[- 1][: len("found extra space")] == "found extra space":
                if self.currentCharacter == " ":
                    pass
                else:
                    charSequence = ""
                    newFile.write(self.currentCharacter)
            elif self.sequence[- 1][: len("found extra tab")] == "found extra tab":
                if self.xtraTabSpace:
                    charSequence = "    " * (self.spaceCounter // 4)

                if self.xtraTab:
                    charSequence = "    " * (self.prevTabLen + 1)
                newFile.write(charSequence + self.currentCharacter)
                charSequence = ""
                self.xtraTab = False
                self.xtraTabSpace = False
            elif self.currentCharacter in self.foundXtraSpaceChars and len(charSequence) > 0:
                charSequence = ""
                newFile.write(self.currentCharacter)
            elif (self.currentState() != "found space" or self.currentState() != "found tab") and len(charSequence) > 0:
                newFile.write(charSequence + self.currentCharacter)
                charSequence = ""
            else:
                newFile.write(self.currentCharacter)

        file.close()
        newFile.close()
        self.document.add_paragraph(self.sequence)
        self.document.save(newFileName[0] + " clean list of states.docx")