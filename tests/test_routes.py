import json
import pytest
from flask import Flask
from routes import register_routes, api


# App fixture

@pytest.fixture
def app():
    """Create a minimal Flask app with all routes registered for testing."""
    application = Flask(__name__, template_folder="../templates")
    application.config["TESTING"] = True
    application.config["SECRET_KEY"] = "test-secret"
    register_routes(application)
    return application


@pytest.fixture
def client(app):
    return app.test_client()


# Helper


def post_json(client, url, body):
    return client.post(
        url,
        data=json.dumps(body),
        content_type="application/json",
    )


# 1. Health check

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200

    def test_health_ok_true(self, client):
        data = res = client.get("/api/health").get_json()
        assert data["ok"] is True

    def test_health_contains_status(self, client):
        data = client.get("/api/health").get_json()
        assert data["status"] == "running"



# 2. /api/meta

class TestMetaEndpoint:

    def test_meta_returns_200(self, client):
        res = client.get("/api/meta")
        assert res.status_code == 200

    def test_meta_ok_flag(self, client):
        data = client.get("/api/meta").get_json()
        assert data["ok"] is True

    def test_meta_contains_genres(self, client):
        data = client.get("/api/meta").get_json()
        assert "genres" in data
        assert len(data["genres"]) > 0

    def test_meta_contains_scales(self, client):
        data = client.get("/api/meta").get_json()
        assert "scales" in data
        assert "C Minor" in data["scales"]

    def test_meta_contains_instruments(self, client):
        data = client.get("/api/meta").get_json()
        assert "instruments" in data
        assert set(data["instruments"]) == {"melody", "bass", "drums", "chords"}

    def test_meta_contains_orders(self, client):
        data = client.get("/api/meta").get_json()
        assert data["orders"] == [1, 2, 3]



# 3. /api/generate  (POST)

class TestGenerateEndpoint:

    def test_valid_request_returns_200(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz", "scale": "C Minor", "order": 1, "steps": 8
        })
        assert res.status_code == 200

    def test_valid_request_ok_true(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Ambient", "scale": "C Major", "order": 2, "steps": 10
        })
        data = res.get_json()
        assert data["ok"] is True

    def test_result_key_present(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "House", "scale": "C Minor", "order": 1, "steps": 8
        })
        data = res.get_json()
        assert "result" in data

    def test_result_contains_sequences(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Hip Hop", "scale": "C Minor", "order": 1, "steps": 16
        })
        data = res.get_json()
        assert "sequences" in data["result"]

    def test_sequence_length_matches_steps(self, client):
        steps = 24
        res = post_json(client, "/api/generate", {
            "genre": "Ambient", "scale": "C Minor", "order": 1, "steps": steps
        })
        data = res.get_json()
        for inst, seq in data["result"]["sequences"].items():
            assert len(seq) == steps, f"Wrong length for {inst}"

    def test_missing_genre_returns_400(self, client):
        res = post_json(client, "/api/generate", {"scale": "C Minor"})
        assert res.status_code == 400
        data = res.get_json()
        assert data["ok"] is False

    def test_missing_scale_returns_400(self, client):
        res = post_json(client, "/api/generate", {"genre": "Ambient"})
        assert res.status_code == 400
        data = res.get_json()
        assert data["ok"] is False

    def test_invalid_genre_returns_400(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "FakeGenre", "scale": "C Minor"
        })
        assert res.status_code == 400
        data = res.get_json()
        assert data["ok"] is False

    def test_invalid_scale_returns_400(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Ambient", "scale": "Z Scale"
        })
        assert res.status_code == 400
        data = res.get_json()
        assert data["ok"] is False

    def test_default_order_applied_when_omitted(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz", "scale": "C Minor"
        })
        data = res.get_json()
        assert data["result"]["order"] == 2  # default

    def test_default_steps_applied_when_omitted(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Techno-Jazz", "scale": "C Minor"
        })
        data = res.get_json()
        assert data["result"]["steps"] == 16  # default

    def test_seed_produces_reproducible_result(self, client):
        body = {"genre": "House", "scale": "C Minor", "order": 2, "steps": 20, "seed": 77}
        r1 = post_json(client, "/api/generate", body).get_json()
        r2 = post_json(client, "/api/generate", body).get_json()
        assert r1["result"]["sequences"] == r2["result"]["sequences"]

    def test_active_instruments_subset(self, client):
        res = post_json(client, "/api/generate", {
            "genre": "Ambient", "scale": "C Minor",
            "order": 1, "steps": 8,
            "instruments": ["melody", "bass"]
        })
        data = res.get_json()
        assert set(data["result"]["sequences"].keys()) == {"melody", "bass"}

    def test_empty_body_returns_400(self, client):
        res = post_json(client, "/api/generate", {})
        assert res.status_code == 400



# 4. /api/step  (POST)

class TestStepEndpoint:

    def test_valid_step_returns_200(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Techno-Jazz", "scale": "C Minor", "order": 1,
            "current": {"melody": "Do", "bass": "Do", "drums": "Closed", "chords": "i"},
            "instruments": ["melody", "bass", "drums", "chords"]
        })
        assert res.status_code == 200

    def test_step_ok_true(self, client):
        res = post_json(client, "/api/step", {
            "genre": "House", "scale": "C Minor", "order": 2,
            "current": {"melody": "Do", "bass": "Do", "drums": "Closed", "chords": "i"},
        })
        data = res.get_json()
        assert data["ok"] is True

    def test_step_returns_states_and_labels(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Ambient", "scale": "C Minor", "order": 1,
            "current": {"melody": "Do", "bass": "Do", "drums": "Closed", "chords": "i"},
        })
        data = res.get_json()
        assert "states" in data
        assert "labels" in data

    def test_step_missing_genre_returns_400(self, client):
        res = post_json(client, "/api/step", {"scale": "C Minor"})
        assert res.status_code == 400

    def test_step_invalid_genre_returns_400(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Nonexistent", "scale": "C Minor", "order": 1
        })
        assert res.status_code == 400

    def test_step_labels_are_strings(self, client):
        res = post_json(client, "/api/step", {
            "genre": "Hip Hop", "scale": "C Major", "order": 1,
            "current": {"melody": "Do", "bass": "Do", "drums": "Closed", "chords": "i"},
        })
        data = res.get_json()
        for label in data["labels"].values():
            assert isinstance(label, str)


# 5. /api/graph  (GET)

class TestGraphEndpoint:

    def test_valid_request_returns_200(self, client):
        res = client.get("/api/graph?genre=Techno-Jazz&scale=C+Minor&order=1")
        assert res.status_code == 200

    def test_valid_request_ok_true(self, client):
        data = client.get("/api/graph?genre=House&scale=C+Minor&order=2").get_json()
        assert data["ok"] is True

    def test_graph_key_present(self, client):
        data = client.get("/api/graph?genre=Ambient&scale=C+Major&order=1").get_json()
        assert "graph" in data

    def test_missing_genre_returns_400(self, client):
        res = client.get("/api/graph?scale=C+Minor")
        assert res.status_code == 400

    def test_missing_scale_returns_400(self, client):
        res = client.get("/api/graph?genre=Ambient")
        assert res.status_code == 400

    def test_invalid_genre_returns_400(self, client):
        res = client.get("/api/graph?genre=FakeGenre&scale=C+Minor")
        assert res.status_code == 400

    def test_default_order_is_2(self, client):
        data = client.get("/api/graph?genre=Ambient&scale=C+Minor").get_json()
        assert data["graph"]["order"] == 2

    def test_graph_contains_all_instruments(self, client):
        data = client.get("/api/graph?genre=Techno-Jazz&scale=C+Minor&order=1").get_json()
        graphs = data["graph"]["graphs"]
        assert set(graphs.keys()) == {"melody", "bass", "drums", "chords"}



# 6. /api/settings  (GET, POST, POST reset)

class TestSettingsEndpoint:

    def test_get_settings_returns_200(self, client):
        res = client.get("/api/settings")
        assert res.status_code == 200

    def test_get_settings_ok_true(self, client):
        data = client.get("/api/settings").get_json()
        assert data["ok"] is True

    def test_post_settings_saves_data(self, client):
        post_json(client, "/api/settings", {"theme": "dark", "volume": 80})
        data = client.get("/api/settings").get_json()
        assert data["settings"]["theme"] == "dark"
        assert data["settings"]["volume"] == 80

    def test_post_settings_returns_200(self, client):
        res = post_json(client, "/api/settings", {"bpm": 120})
        assert res.status_code == 200

    def test_reset_settings_clears_data(self, client):
        post_json(client, "/api/settings", {"theme": "dark"})
        post_json(client, "/api/settings/reset", {})
        data = client.get("/api/settings").get_json()
        assert data["settings"] == {}

    def test_reset_settings_returns_200(self, client):
        res = post_json(client, "/api/settings/reset", {})
        assert res.status_code == 200


# 7. /api/sessions  (GET, POST, DELETE)

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

    def test_list_sessions_ok_true(self, client):
        data = client.get("/api/sessions").get_json()
        assert data["ok"] is True

    def test_list_sessions_has_count(self, client):
        data = client.get("/api/sessions").get_json()
        assert "count" in data

    def test_save_session_returns_201_or_200(self, client):
        res = self._save_session(client)
        assert res.status_code in (200, 201)

    def test_save_session_increments_count(self, client):
        before = client.get("/api/sessions").get_json()["count"]
        self._save_session(client)
        after = client.get("/api/sessions").get_json()["count"]
        assert after == before + 1

    def test_saved_session_has_id(self, client):
        res = self._save_session(client)
        data = res.get_json()
        assert "session" in data
        assert "id" in data["session"]

    def test_delete_existing_session(self, client):
        session_id = self._save_session(client).get_json()["session"]["id"]
        res = client.delete(f"/api/sessions/{session_id}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["ok"] is True

    def test_delete_nonexistent_session_returns_404(self, client):
        res = client.delete("/api/sessions/9999999999")
        assert res.status_code == 404

    def test_clear_all_sessions(self, client):
        self._save_session(client, "A")
        self._save_session(client, "B")
        client.delete("/api/sessions")
        count = client.get("/api/sessions").get_json()["count"]
        assert count == 0

    def test_sessions_capped_at_100(self, client):
        # Save 105 sessions and check the list stays at <=100
        for i in range(105):
            post_json(client, "/api/sessions", {"name": f"Session {i}"})
        count = client.get("/api/sessions").get_json()["count"]
        assert count <= 100