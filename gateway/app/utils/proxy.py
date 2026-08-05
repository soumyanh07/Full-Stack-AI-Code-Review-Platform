import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger("gateway.proxy")


class ProxyClient:
    @staticmethod
    async def forward(
        method: str,
        url: str,
        headers: Optional[dict] = None,
        body: Any = None,
        params: Optional[dict] = None,
        timeout: float = 5.0,
    ) -> tuple[dict | list | Any, int]:
        request_headers = dict(headers or {})
        if body is not None and "content-type" not in {
            key.lower(): value for key, value in request_headers.items()
        }:
            request_headers["content-type"] = "application/json"

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(connect=timeout, read=timeout, write=timeout, pool=timeout)
            ) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=body,
                    params=params,
                    headers=request_headers,
                )

                try:
                    payload = response.json()
                except ValueError:
                    payload = {"detail": response.text or "Empty response from auth service"}

                logger.info("Proxy %s %s -> %s", method.upper(), url, response.status_code)
                return payload, response.status_code
        except httpx.TimeoutException:
            logger.exception("Proxy request to %s timed out", url)
            return {"detail": "Auth service request timed out"}, 504
        except httpx.RequestError as exc:
            logger.exception("Proxy request to %s failed", url)
            return {"detail": f"Unable to reach auth service: {exc}"}, 502