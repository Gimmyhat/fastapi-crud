import json
import pytest

from app.api import crud_dish

prefix = "/api/v1/menus/1/submenus/1/dishes"
crud = crud_dish


def test_read_all_dishes(test_app, monkeypatch):
    test_data = []

    def mock_get_all(db_session, submenu_id):
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_create_dish(test_app, monkeypatch):
    test_request_payload = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    test_response_payload = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
        "id": "1"
    }

    def mock_post(db_session, payload, menu_id, submenu_id):
        return test_response_payload

    monkeypatch.setattr(crud, "post", mock_post)
    response = test_app.post(f"{prefix}/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json().get('id')
    assert response.json().get('title')
    assert response.json().get('description')
    assert response.json().get('price')


def test_create_dish_invalid_json(test_app):
    response = test_app.post(f"{prefix}/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422

    response = test_app.post(
        f"{prefix}", content=json.dumps({"title": "1", "description": "2"})
    )
    assert response.status_code == 422


def test_read_dish(test_app, monkeypatch):
    test_data = {
        "title": "string",
        "description": "string",
        "id": "string",
        "price": "12.50"
    }

    def mock_get(db_session, id, submenu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(f"{prefix}/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_dish_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id, submenu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(f"{prefix}/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


def test_update_dish(test_app, monkeypatch):
    test_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
        "id": "1"
    }
    test_update_data = {
        "title": "My dish 1 update",
        "description": "My dish description 1 update",
        "price": "12.50",
        "id": "1"
    }

    def mock_get(db_session, id, submenu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_put(db_session, dish, title, description, price):
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
        [999, {"title": "foo", "description": "bar", "price": "12.50"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_dish_invalid(test_app, monkeypatch, id, payload, status_code):
    def mock_get(db_session, id, submenu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.patch(f"{prefix}/{id}/", content=json.dumps(payload), )
    assert response.status_code == status_code


def test_remove_dish(test_app, monkeypatch):
    test_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
        "id": "1"
    }

    def mock_get(db_session, id, submenu_id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    def mock_delete(db_session, dish):
        return test_data

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(f"{prefix}/1/")
    assert response.status_code == 200


def test_remove_dish_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id, submenu_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(f"{prefix}/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"

    response = test_app.delete(f"{prefix}/0/")
    assert response.status_code == 422
