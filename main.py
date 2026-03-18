import sys
from tokenizer import tokenize, TokenType
from parser import Parser
from interpreter import Interpreter

if len(sys.argv) < 2:
    print("Usage: python main.py <file.lsc>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename,"r") as f:
    source =f.read()

tokens = tokenize(source)
parser= Parser(tokens)
result = parser.parse()

interpreter = Interpreter(result)
interpreter.run()

