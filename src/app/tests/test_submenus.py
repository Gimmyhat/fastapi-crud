import json

import pytest
from ..api import crud_submenu

prefix = "/api/v1/menus/1/submenus"
crud = crud_submenu


def test_read_all_submenus(test_app, monkeypatch):
    test_data = []

    def mock_get_all(db_session, menu_id):
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_create_submenu(test_app, monkeypatch):
    test_request_payload = {"title": "My submenu 1", "description": "My submenu description 1"}
    test_response_payload = {"title": "My submenu 1", "description": "My submenu description 1", "id": '1'}

    def mock_post(db_session, payload, menu_id):
        return test_response_payload

    monkeypatch.setattr(crud, "post", mock_post)
    response = test_app.post(f"{prefix}/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json().get('id')
    assert response.json().get('title')
    assert response.json().get('description')


def test_create_submenu_invalid_json(test_app):
    response = test_app.post(f"{prefix}/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422

    response = test_app.post(
        f"{prefix}", content=json.dumps({"title": "1", "description": "2"})
    )
    assert response.status_code == 422


def test_read_submenu(test_app, monkeypatch):
    test_data = {
        "title": "string",
        "description": "string",
        "id": "string",
        "dishes_count": 0
    }

    def mock_get(db_session, id, menu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(f"{prefix}/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_submenu_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id, menu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(f"{prefix}/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


def test_update_submenu(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": "1"}
    test_update_data = {"title": "someone", "description": "someone else", "id": "1"}

    def mock_get(db_session, id, menu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_put(db_session, submenu, title, description):
        return test_update_data

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.patch(f"{prefix}/1/", content=json.dumps(test_update_data), )
    assert response.status_code == 200
    assert response.json()['title'] == test_update_data['title']
    assert response.json()['description'] == test_update_data['description']


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_submenu_invalid(test_app, monkeypatch, id, payload, status_code):
    def mock_get(db_session, id, menu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.patch(f"{prefix}/{id}/", content=json.dumps(payload), )
    assert response.status_code == status_code


def test_remove_submenu(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": '1'}

    def mock_get(db_session, id, menu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_delete(db_session, submenu):
        return test_data

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(f"{prefix}/1/")
    assert response.status_code == 200


def test_remove_submenu_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id, menu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(f"{prefix}/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"

    response = test_app.delete(f"{prefix}/0/")
    assert response.status_code == 422
