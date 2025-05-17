import random
import requests
import pytest
from config import BASE_URL, HEADERS

@pytest.fixture(scope="module")
def pet_payload():
    pet_id = random.randint(100000, 999999)
    return {
        "id": pet_id,
        "name": f"TestPet{pet_id}",
        "photoUrls": [],
        "status": "available"
    }

@pytest.fixture(scope="module")
def created_pet(pet_payload):
    #CREATE
    resp = requests.post(f'{BASE_URL}/pet', json=pet_payload, headers=HEADERS)
    assert resp.status_code == 200, "Не удалось создать pet"
    yield pet_payload
    #TEARDOWN
    requests.delete(f"{BASE_URL}/pet/{pet_payload['id']}")

def test_get_pet_by_id(created_pet):
    pet_id = created_pet["id"]
    resp = requests.get(f"{BASE_URL}/pet/{pet_id}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == pet_id
    assert data["name"] == created_pet["name"]

def test_update_pet_status(created_pet):
    """PUT /pet — меняем статус на 'sold'"""
    pet_id = created_pet["id"]
    updated = {**created_pet, "status": "sold"}
    resp = requests.put(f"{BASE_URL}/pet", json=updated, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "sold"

def test_delete_pet():
    """DELETE /pet/{petId} — создаём, удаляем и проверяем отсутствие."""
    # Сначала создаём временного питомца
    temp_id = random.randint(100000, 999999)
    temp = {
        "id": temp_id,
        "name": f"Tmp{temp_id}",
        "photoUrls": [],
        "status": "available"
    }
    # CREATE
    resp = requests.post(f"{BASE_URL}/pet", json=temp, headers=HEADERS)
    assert resp.status_code == 200, f"Не удалось создать временного питомца: {resp.status_code}"

    # DELETE
    resp = requests.delete(f"{BASE_URL}/pet/{temp_id}", headers=HEADERS)
    assert resp.status_code == 200, f"Не удалось удалить питомца: {resp.status_code}"

    # VERIFY
    resp = requests.get(f"{BASE_URL}/pet/{temp_id}", headers=HEADERS)
    assert resp.status_code == 404, f"Ожидали 404 после удаления, получили {resp.status_code}"
