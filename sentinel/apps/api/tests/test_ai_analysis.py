from unittest.mock import AsyncMock, patch

import httpx
import pytest

from sentinel_api.services.ai_analysis import generate_security_explanation


@pytest.mark.asyncio
async def test_disabled_provider_returns_none():
    with patch("sentinel_api.services.ai_analysis.get_settings") as get_settings:
        get_settings.return_value.ai_provider = "mock"
        get_settings.return_value.ai_api_key = None
        get_settings.return_value.ai_model = "unused"
        assert await generate_security_explanation({"verdict": "suspicious"}) is None


@pytest.mark.asyncio
async def test_google_provider_returns_model_text():
    settings = type("Settings", (), {
        "ai_provider": "google",
        "ai_api_key": "test-key",
        "ai_model": "configured-carbon-model-id",
    })()
    response = httpx.Response(
        200,
        json={"candidates": [{"content": {"parts": [{"text": "Review sender alignment."}]}}]},
        request=httpx.Request("POST", "https://example.test"),
    )
    with patch("sentinel_api.services.ai_analysis.get_settings", return_value=settings), \
         patch("sentinel_api.services.ai_analysis.httpx.AsyncClient") as client_cls:
        client = client_cls.return_value.__aenter__.return_value
        client.post = AsyncMock(return_value=response)
        result = await generate_security_explanation({"verdict": "suspicious"})
    assert result == "Review sender alignment."
    assert client.post.await_count == 1


@pytest.mark.asyncio
async def test_provider_failure_fails_closed():
    settings = type("Settings", (), {
        "ai_provider": "google",
        "ai_api_key": "test-key",
        "ai_model": "configured-carbon-model-id",
    })()
    with patch("sentinel_api.services.ai_analysis.get_settings", return_value=settings), \
         patch("sentinel_api.services.ai_analysis.httpx.AsyncClient") as client_cls:
        client = client_cls.return_value.__aenter__.return_value
        client.post = AsyncMock(side_effect=httpx.ConnectError("offline"))
        assert await generate_security_explanation({"verdict": "suspicious"}) is None
