from flask import Flask, request, jsonify, render_template
from tokenizer import tokenize
from parser import Parser
from interpreter import Interpreter
import io
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods =["POST"])
def run():
    data = request.get_json()
    source = data.get("source","")

    try:
        tokens = tokenize(source)
        parser = Parser(tokens)
        result= parser.parse()

        #capture print output from interpreter
        output = io.StringIO()
        sys.stdout = output
        interpreter = Interpreter(result)
        interpreter.run()
        sys.stdout = sys.__stdout__
        return jsonify({"output": output.getvalue(), "error":None})
    
    except Exception as e:
        sys.stdout = sys.__stdout__
        return jsonify({"output": None, "error": str(e)})
    

if __name__ == "__main__":
    app.run(debug=True)