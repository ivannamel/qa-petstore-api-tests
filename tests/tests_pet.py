# tests/test_pet.py

import requests
from requests import Response
from config import BASE_URL, DEFAULT_STATUS

def test_find_pets_by_status():
    resp: Response = requests.get(
        f"{BASE_URL}/pet/findByStatus",
        params={"status": DEFAULT_STATUS}
    )

    assert resp.status_code == 200
    pets = resp.json()

    assert isinstance(pets, list)

    # Исправленное выражение
    assert any(pet.get("status") == DEFAULT_STATUS for pet in pets), \
        f"No pet has status {DEFAULT_STATUS}"
