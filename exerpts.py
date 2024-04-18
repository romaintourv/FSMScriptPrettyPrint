
        if self.currentState() == "in multiline comment" and currentChar != self.prevChar:
            self.state = "in multiline comment"
            self.sequence.append(self.state)
            return

# found string or comment
        elif (currentChar == "\'" or currentChar == '\"') and self.currentState() != "in string" and self.currentState() != "found string" and self.currentState() != "found string 2":
            self.state = "found string"
            self.sequence.append(self.state)
            self.prevChar = currentChar

        # found string 2
        elif self.currentState() == "found string" and (currentChar == self.prevChar):
            self.state = "found string 2"
            self.sequence.append(self.state)
        
        elif self.currentState() == "found string 2" and (currentChar == self.prevChar):
            self.state = "in multiline comment"
            self.sequence.append(self.state)
        
        elif self.currentState() == "found string 2" and (currentChar != self.prevChar):
            
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
            
            self.sequence.append(self.state)
        
        elif self.currentState() == "in multiline comment" and currentChar == self.prevChar:
            self.state = "out of comment"
            self.sequence.append(self.state)
        
        elif self.currentState() == "out of comment" and currentChar == self.prevChar:
            self.state = "out of comment 2"
            self.sequence.append(self.state)
        
        elif self.currentState() == "out of comment" and currentChar != self.prevChar:
            self.state = "in multiline comment"
            self.sequence.append(self.state)
        
        elif self.currentState() == "out of comment 2" and currentChar == self.prevChar:
            self.state = "out of comment 3"
            self.sequence.append(self.state)

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

        elif self.currentState() == "out of comment 2" and currentChar != self.prevChar:
            self.state = "in multiline comment"
            self.sequence.append(self.state)
