import json
import pytest
from flask import Flask
from routes import register_routes


@pytest.fixture
def app():
    application = Flask(__name__, template_folder="../templates")
    application.config["TESTING"] = True
    application.config["SECRET_KEY"] = "test-secret"
    register_routes(application)
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def post_json(client, url, body):
    return client.post(
        url,
        data=json.dumps(body),
        content_type="application/json",
    )


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200

    def test_health_ok_true(self, client):
        data = client.get("/api/health").get_json()
        assert data["ok"] is True

    def test_health_contains_status(self, client):
        data = client.get("/api/health").get_json()
        assert data["status"] == "running"


class TestMetaEndpoint:
    def test_meta_returns_200(self, client):
        res = client.get("/api/meta")
        assert res.status_code == 200

    def test_meta_contains_genres(self, client):
        data = client.get("/api/meta").get_json()
        assert "genres" in data
        assert len(data["genres"]) > 0

    def test_meta_contains_scales(self, client):
        data = client.get("/api/meta").get_json()
        assert "scales" in data

    def test_meta_contains_instruments(self, client):
        data = client.get("/api/meta").get_json()
        assert set(data["instruments"]) == {"melody", "bass", "drums", "chords"}

    def test_meta_contains_orders(self, client):
        data = client.get("/api/meta").get_json()
        assert data["orders"] == [1, 2, 3]


class TestGenerateEndpoint:
    def test_valid_request_returns_200(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz",
            "scale": "C Minor",
            "order": 1,
            "steps": 8
        })
        assert res.status_code == 200

    def test_result_contains_sequences(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Hip Hop",
            "scale": "C Minor",
            "order": 1,
            "steps": 16
        })
        data = res.get_json()
        assert "sequences" in data["result"]

    def test_missing_genre_returns_400(self, client):
        res = post_json(client, "/api/generate", {"scale": "C Minor"})
        assert res.status_code == 400

    def test_invalid_genre_returns_400(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "FakeGenre",
            "scale": "C Minor"
        })
        assert res.status_code == 400

    def test_default_order_applied_when_omitted(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz",
            "scale": "C Minor"
        })
        data = res.get_json()
        assert data["result"]["order"] == 2

    def test_default_steps_applied_when_omitted(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz",
            "scale": "C Minor"
        })
        data = res.get_json()
        assert data["result"]["steps"] == 16


class TestStepEndpoint:
    def test_valid_step_returns_200(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Techno-Jazz",
            "scale": "C Minor",
            "order": 1,
            "current": {
                "melody": "Do",
                "bass": "Do",
                "drums": "Closed",
                "chords": "i"
            }
        })
        assert res.status_code == 200

    def test_step_returns_states_and_labels(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Ambient",
            "scale": "C Minor",
            "order": 1,
            "current": {
                "melody": "Do",
                "bass": "Do",
                "drums": "Closed",
                "chords": "i"
            }
        })
        data = res.get_json()
        assert "states" in data
        assert "labels" in data

    def test_step_missing_genre_returns_400(self, client):
        res = post_json(client, "/api/step", {"scale": "C Minor"})
        assert res.status_code == 400


class TestGraphEndpoint:
    def test_valid_request_returns_200(self, client):
        res = client.get("/api/graph?genre=Techno-Jazz&scale=C+Minor&order=1")
        assert res.status_code == 200

    def test_graph_key_present(self, client):
        data = client.get("/api/graph?genre=Ambient&scale=C+Major&order=1").get_json()
        assert "graph" in data

    def test_missing_genre_returns_400(self, client):
        res = client.get("/api/graph?scale=C+Minor")
        assert res.status_code == 400


class TestSettingsEndpoint:
    def test_get_settings_returns_200(self, client):
        res = client.get("/api/settings")
        assert res.status_code == 200

    def test_post_settings_saves_data(self, client):
        post_json(client, "/api/settings", {"theme": "dark", "volume": 80})
        data = client.get("/api/settings").get_json()
        assert data["settings"]["theme"] == "dark"
        assert data["settings"]["volume"] == 80

    def test_reset_settings_clears_data(self, client):
        post_json(client, "/api/settings", {"theme": "dark"})
        post_json(client, "/api/settings/reset", {})
        data = client.get("/api/settings").get_json()
        assert data["settings"] == {}


class TestSessionsEndpoint:
    def _save_session(self, client, name="Test Session"):
        return post_json(client, "/api/sessions", {
            "name": name,
            "genre": "Ambient",
            "scale": "C Minor",
            "sequences": {"melody": ["Do", "Fa"]},
        })

    def test_list_sessions_returns_200(self, client):
        res = client.get("/api/sessions")
        assert res.status_code == 200

    def test_save_session_returns_200_or_201(self, client):
        res = self._save_session(client)
        assert res.status_code in (200, 201)

    def test_saved_session_has_id(self, client):
        res = self._save_session(client)
        data = res.get_json()
        assert "session" in data
        assert "id" in data["session"]

    def test_delete_existing_session(self, client):
        session_id = self._save_session(client).get_json()["session"]["id"]
        res = client.delete(f"/api/sessions/{session_id}")
        assert res.status_code == 200