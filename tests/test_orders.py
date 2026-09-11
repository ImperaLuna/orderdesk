from httpx import AsyncClient


async def _user(client: AsyncClient) -> str:
    r = await client.post("/api/v1/users", json={"email": "o@example.com", "display_name": "O"})
    return str(r.json()["id"])


async def test_place_and_page_orders(client: AsyncClient) -> None:
    uid = await _user(client)
    for cents in (100, 200, 300):
        r = await client.post(
            "/api/v1/orders", json={"user_id": uid, "currency": "usd", "total_cents": cents}
        )
        assert r.status_code == 201, r.text
        assert r.json()["currency"] == "USD"

    r = await client.get("/api/v1/orders", params={"limit": 2})
    page = r.json()
    assert [o["total_cents"] for o in page["items"]] == [100, 200]
    assert page["next_cursor"] == page["items"][-1]["id"]

    r = await client.get("/api/v1/orders", params={"limit": 2, "after": page["next_cursor"]})
    assert [o["total_cents"] for o in r.json()["items"]] == [300]
    assert r.json()["next_cursor"] is None


async def test_status_transitions(client: AsyncClient) -> None:
    uid = await _user(client)
    r = await client.post(
        "/api/v1/orders", json={"user_id": uid, "currency": "EUR", "total_cents": 999}
    )
    oid = r.json()["id"]
    assert (
        await client.post(f"/api/v1/orders/{oid}/status", params={"new_status": "paid"})
    ).status_code == 200
    assert (
        await client.post(f"/api/v1/orders/{oid}/status", params={"new_status": "pending"})
    ).status_code == 409
    events = (await client.get(f"/api/v1/orders/{oid}/events")).json()
    assert [e["kind"] for e in events] == ["created", "status_changed"]


async def test_unknown_user_rejected(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/orders",
        json={
            "user_id": "00000000-0000-4000-8000-000000000000",
            "currency": "USD",
            "total_cents": 1,
        },
    )
    assert r.status_code == 404
