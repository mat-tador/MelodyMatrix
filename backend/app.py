from flask import Flask
from flask_cors import CORS
from guest_routes import guest_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(guest_bp, url_prefix="/guest")

@app.route("/")
def home():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    app.run(debug=True)