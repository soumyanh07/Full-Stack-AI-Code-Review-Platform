import httpx


class ProxyClient:
    @staticmethod
    async def forward(
        method: str,
        url: str,
        headers=None,
        body=None,
        params=None,
    ):
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body,
                params=params,
            )
            try:
                payload = response.json()
            except ValueError:
                payload = {"detail": response.text}
            return payload, response.status_code