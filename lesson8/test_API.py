import requests
import pytest


BASE_URL = "https://ru.yougile.com/api-v2"
TOKEN = ""
HEADERS = {"Authorization": f"Bearer {TOKEN}"} 

def test_create_project_post():
    payload = {
        "title": "autotest"
    }
    r = requests.post(
        f"{BASE_URL}/projects",
        json=payload,
        headers=HEADERS,
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert isinstance(body.get("id"), str)
    assert body["id"]


def test_create_project_post__400_without_title():
    payload = {"users": {}}
    r = requests.post(
        f"{BASE_URL}/projects",
        json=payload,
        headers=HEADERS,
    )
    assert r.status_code == 400, r.text

def test_get_project_get__200():
    r_create = requests.post(
        f"{BASE_URL}/projects",
        json={"title": "autotest"},
        headers=HEADERS,
    )
    assert r_create.status_code == 201, r_create.text
    project_id = r_create.json()["id"]

    r_get = requests.get(
        f"{BASE_URL}/projects/{project_id}",
        headers=HEADERS,
    )
    assert r_get.status_code == 200, r_get.text
    assert r_get.json().get("id") == project_id


def test_get_project_get__404_unknown_id():
    bogus_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    r = requests.get(
        f"{BASE_URL}/projects/{bogus_id}",
        headers=HEADERS,
    )
    assert r.status_code == 404, r.text

def test_update_project_put():
    create_payload = {
        "title": "autotest",
        "users": {},
    }
    r_create = requests.post(
        f"{BASE_URL}/projects",
        json=create_payload,
        headers=HEADERS,
    )
    assert r_create.status_code == 201, r_create.text
    project_id = r_create.json()["id"]

    new_title = create_payload["title"] + "_upd"
    r_put = requests.put(
        f"{BASE_URL}/projects/{project_id}",
        json={"title": new_title},
        headers=HEADERS,
    )
    assert r_put.status_code == 200, r_put.text
    assert r_put.json().get("id") == project_id


def test_update_project_put__404_unknown_id():
    bogus_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    r = requests.put(
        f"{BASE_URL}/projects/{bogus_id}",
        json={"title": "x"},
        headers=HEADERS,
    )

    assert r.status_code == 404, r.text
