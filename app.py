from flask import Flask, request, jsonify


app = Flask(__name__)


def predict_clickbait(text):
    return text

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    text = data["text"]
    result = predict_clickbait(text)
    return jsonify({"input": text, "prediction": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 
