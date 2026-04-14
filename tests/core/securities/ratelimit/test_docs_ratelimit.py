async def test_docs_ratelimit(test_client):
    last_status_code = 0
    for i in range(6):
        url = "/auth/login/"
        resp = await test_client.get(url)
        print(resp.status_code)

        last_status_code = resp.status_code

    assert last_status_code == 429
