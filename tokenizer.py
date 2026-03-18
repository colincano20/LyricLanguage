from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    SECTION = "SECTION"
    STRING = "STRING"
    NUMBER = "NUMBER"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    ARROW = "ARROW"


class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line =line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"

KEYWORDS = {"song", "meta", "structure", "repeat", "bpm", "mood", "key"}
def tokenize(source):
    tokens = []
    i = 0
    line = 1
    while i < len(source):
        char = source[i]
        #skip whitespace
        if char in (' ','\t','\r'):
            i+=1
            continue
        if char == '\n':
            line+=1
            i+=1
            continue
        #skip comments with % = comment
        if char == '%':
            while i < len(source) and source[i] != '\n':
                i+=1
            continue
        # Arrow ->
        if char == '-' and i +1 < len(source) and source[i+1] == '>':
            tokens.append(Token(TokenType.ARROW, "->",line))
            i+=2
            continue
        # Braces
        if char == '{':
            tokens.append(Token(TokenType.LBRACE, '{',line))
            i+=1
            continue
        if char == '}':
            tokens.append(Token(TokenType.RBRACE, '}',line))
            i+=1
            continue

        # Strings
        if char == '"':
            i+=1
            start =i
            while i < len(source) and source[i] !='"':
                i+=1
            value = source[start:i]
            tokens.append(Token(TokenType.STRING, value,line))
            i+=1 #skip closing quote
            continue

        #numbers
        if char.isdigit():
            start = i
            while i < len(source) and source[i].isdigit():
                i+=1
            tokens.append(Token(TokenType.NUMBER, int(source[start:i]),line))
            continue

        # Words (keywords or section names)
        if char.isalpha() or char == '_':
            start = i
            while i < len(source) and (source[i].isalnum() or source[i] == '_'):
                i += 1
            word = source[start:i]
            if word in KEYWORDS:
                tokens.append(Token(TokenType.KEYWORD, word,line))
            else:
                tokens.append(Token(TokenType.SECTION, word,line))
            continue

        # If we get here, something unknown
        raise SyntaxError(f"Unexpected character: {repr(char)} at position {i}")

    return tokens
sample = '''
song "Distance"

verse1 {
  "You're 300 miles away"
  repeat 2
}
'''



