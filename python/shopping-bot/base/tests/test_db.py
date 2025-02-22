import pytest
from db import init_db, save_state, load_state
import os
from unittest.mock import patch

@pytest.fixture
def db_setup(tmp_path):
    db_file = tmp_path / "test_db.db"
    os.environ["DB_FILE"] = str(db_file)
    init_db(force_reset=True)
    yield str(db_file)
    if os.path.exists(db_file):
        os.remove(db_file)

def test_save_and_load_state(db_setup):
    session_id = "test_session"
    order = {"rest1:Idli & Vada:1": 1}
    restaurants = {"rest1": {"name": "Test Cafe", "menu": {"Idli & Vada": [{"id": "1", "name": "Butter Idli"}]}}}
    save_state(session_id, order, restaurants, True, "user1", "token123", "rest1", "order1")
    loaded_order, loaded_restaurants, awaiting, user_id, token, selected, order_id = load_state(session_id)
    assert loaded_order == order
    assert loaded_restaurants == restaurants
    assert awaiting is True
    assert user_id == "user1"
    assert token == "token123"
    assert selected == "rest1"
    assert order_id == "order1"

def test_load_state_no_session(db_setup):
    result = load_state("nonexistent_session")
    assert result == ({}, {}, False, None, None, None, None)