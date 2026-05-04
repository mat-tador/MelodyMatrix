import os
os.environ["TEST_MODE"] = "true"

from chatbot import get_chat_result


def test_ai_response():
    res = get_chat_result("What is melody?")
    assert "reply" in res
    assert isinstance(res["reply"], str)


def test_music_query():
    res = get_chat_result("What is BPM?")
    
    if os.getenv("TEST_MODE") == "true":
        assert isinstance(res["reply"], str)
    else:
        assert "bpm" in res["reply"].lower()


def test_config_generation():
    res = get_chat_result("give me a sad preset")
    assert res["config_json"] is not None


def test_config_structure():
    res = get_chat_result("generate json config")
    config = res["config_json"]

    assert isinstance(config, dict)
    assert "bpm" in config
    assert "scale" in config


def test_config_ranges():
    res = get_chat_result("epic cinematic preset")
    config = res["config_json"]

    assert 40 <= config["bpm"] <= 200
    assert 1 <= config["markov_order"] <= 6


def test_empty_input():
    res = get_chat_result("")
    assert res["reply"] == "Please enter a message."


def test_random_input():
    res = get_chat_result("asdasdasd nonsense")
    assert isinstance(res["reply"], str)
