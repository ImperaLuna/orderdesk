from httpx import AsyncClient


async def test_create_and_get_user(client: AsyncClient) -> None:
    r = await client.post("/api/v1/users", json={"email": "a@example.com", "display_name": "A"})
    assert r.status_code == 201
    user_id = r.json()["id"]
    r = await client.get(f"/api/v1/users/{user_id}")
    assert r.status_code == 200
    assert r.json()["email"] == "a@example.com"


async def test_duplicate_email_conflicts(client: AsyncClient) -> None:
    body = {"email": "dup@example.com", "display_name": "D"}
    assert (await client.post("/api/v1/users", json=body)).status_code == 201
    assert (await client.post("/api/v1/users", json=body)).status_code == 409


async def test_random_user_returns_a_user(client: AsyncClient) -> None:
    ids = set()
    for i in range(5):
        r = await client.post(
            "/api/v1/users", json={"email": f"u{i}@example.com", "display_name": str(i)}
        )
        ids.add(r.json()["id"])
    r = await client.get("/api/v1/users/random")
    assert r.status_code == 200
    assert r.json()["id"] in ids


async def test_random_user_404_when_empty(client: AsyncClient) -> None:
    r = await client.get("/api/v1/users/random")
    assert r.status_code == 404
