import pytest
import requests

BASE = "https://restful-booker.herokuapp.com"
BOOKING = {
    "firstname": "Ana", "lastname": "Pop", "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2027-01-10", "checkout": "2027-01-12"},
    "additionalneeds": "Breakfast",
}

@pytest.fixture(scope="session")
def token():
    r = requests.post(f"{BASE}/auth",json={"username": "admin", "password": "password123"}, timeout=15)
    assert r.status_code == 200
    return r.json()["token"]

@pytest.mark.api
def test_health_check():
    assert requests.get(f"{BASE}/ping", timeout=15).status_code == 201

@pytest.mark.api
def test_create_and_read_booking():
    r = requests.post(f"{BASE}/booking", json=BOOKING, timeout=15)
    assert r.status_code == 200
    booking_id = r.json()["bookingid"]
    got = requests.get(f"{BASE}/booking/{booking_id}", timeout=15)
    assert got.status_code == 200
    assert got.json()["firstname"] == "Ana"

@pytest.mark.api
def test_delete_booking(token):
    booking_id = requests.post(f"{BASE}/booking", json=BOOKING, timeout=15).json()["bookingid"]
    r = requests.delete(f"{BASE}/booking/{booking_id}",
                        headers={"Cookie": f"token={token}"}, timeout=15)
    assert r.status_code == 201
    assert requests.get(f"{BASE}/booking/{booking_id}", timeout=15).status_code == 404

@pytest.mark.api
def test_delete_without_token_is_rejected():
    booking_id = requests.post(f"{BASE}/booking", json=BOOKING, timeout=15).json()["bookingid"]
    r = requests.delete(f"{BASE}/booking/{booking_id}", timeout=15)
    assert r.status_code == 403