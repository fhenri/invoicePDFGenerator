import invoice;

from flask import Flask, request, json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hey Invoice Generation App!'

@app.route("/invoice", methods=["POST"])
def generate_invoice():
    
    if request.is_json:
        data = request.json

    else:
        data = json.loads(request.data)

    invoice.generate(data);
    return 'Invoice Generated', 204

if __name__ == "__main__":
    app.run(debug=True)
