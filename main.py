from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Flask API is running!"})

# Example API endpoint
@app.route("/api/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "stranger")
    return jsonify({"message": f"Hello, {name}!"})

# POST example
@app.route("/api/data", methods=["POST"])
def data():
    body = request.json
    return jsonify({"received": body})

if __name__ == "__main__":
    app.run(debug=True)
