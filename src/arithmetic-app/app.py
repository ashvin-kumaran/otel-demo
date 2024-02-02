from flask import Flask, request

app = Flask(__name__)

@app.route('/add')
def add():
    arg1 = request.args.get("arg1")
    arg2 = request.args.get("arg2")
    return f"{float(arg1)+float(arg2)}\n"

@app.route('/subtract')
def subtract():
    arg1 = request.args.get("arg1")
    arg2 = request.args.get("arg2")
    return f"{float(arg1)-float(arg2)}\n"

@app.route('/multiply')
def multiply():
    arg1 = request.args.get("arg1")
    arg2 = request.args.get("arg2")
    return f"{float(arg1)*float(arg2)}\n"

@app.route('/divide')
def divide():
    arg1 = request.args.get("arg1")
    arg2 = request.args.get("arg2")
    return f"{float(arg1)/float(arg2)}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)