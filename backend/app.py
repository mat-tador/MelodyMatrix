from flask import Flask
from flask_cors import CORS
from routes import register_routes

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = "melody-matrix-secret-2024"
    app.config["JSON_SORT_KEYS"] = False

    # Allow cross-origin requests from the frontend (useful during dev)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    register_routes(app)
    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5001)