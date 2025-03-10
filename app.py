from flask import Flask, request, jsonify
import tensorflow as tf
import pickle

app = Flask(__name__)

# Load the trained model once
model = None
tokenizer = None

def load_resources():
    global model, tokenizer
    if model is None:
        model = tf.keras.models.load_model("clickbait_lstm_model2.h5")
    if tokenizer is None:
        with open("tokenizer2.pkl", "rb") as file:
            tokenizer = pickle.load(file)

def predict_clickbait(text):
    load_resources()  # Ensure model and tokenizer are loaded
    test_input = [text]
    test_sequence = tokenizer.texts_to_sequences(test_input)
    test_padded = tf.keras.preprocessing.sequence.pad_sequences(test_sequence, maxlen=100)
    output = model.predict(test_padded)
    prediction = "Possible Clickbait" if output[0][0] < 0.9327575 else "Not Clickbait"
    return prediction

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
