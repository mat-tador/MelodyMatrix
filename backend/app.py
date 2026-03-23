from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    # Temporary reply
    return jsonify({
        "reply": f'You said: "{message}". Your chatbot backend is working.'
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)