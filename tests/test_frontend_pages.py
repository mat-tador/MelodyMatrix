import os

def test_dashboard_exists():
    assert os.path.exists("frontend/public/dashboard.html")

def test_generate_exists():
    assert os.path.exists("frontend/public/generate.html")

def test_saved_outputs_exists():
    assert os.path.exists("frontend/public/saved-outputs.html")

def test_settings_exists():
    assert os.path.exists("frontend/public/settings.html")


def test_dashboard_content():
    with open("frontend/public/dashboard.html") as f:
        content = f.read()
        assert "Melody Matrix" in content
        assert "Generation Controls" in content


def test_generate_content():
    with open("frontend/public/generate.html") as f:
        content = f.read()
        assert "Generate" in content


def test_saved_outputs_content():
    with open("frontend/public/saved-outputs.html") as f:
        content = f.read()
        assert "Saved Outputs" in content


def test_settings_content():
    with open("frontend/public/settings.html") as f:
        content = f.read()
        assert "Settings" in content