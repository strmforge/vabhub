"""
健康检查端点测试
SYSTEM-AUDIT-FOLLOWUP-1 P2 验证
"""
import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture
async def client():
    """创建测试客户端"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_returns_200(client):
    """测试 /api/health 端点始终返回 200"""
    resp = await client.get("/api/health/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert "version" in data
    assert "time" in data
    assert "uptime_seconds" in data


@pytest.mark.asyncio
async def test_health_contains_db_info(client):
    """测试 /api/health 端点包含数据库信息"""
    resp = await client.get("/api/health/")
    assert resp.status_code == 200
    data = resp.json()
    assert "db" in data
    assert "ok" in data["db"]
    # 如果 DB 正常，应该有 latency_ms
    if data["db"]["ok"]:
        assert "latency_ms" in data["db"]


@pytest.mark.asyncio
async def test_health_full_returns_200(client):
    """测试 /api/health/full 端点返回 200"""
    resp = await client.get("/api/health/full")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("ok", "degraded")
    assert "db" in data
    assert "cache" in data
    assert "disk" in data


@pytest.mark.asyncio
async def test_health_db_check(client):
    """测试 /api/health/db 单项检查"""
    resp = await client.get("/api/health/db")
    assert resp.status_code == 200
    data = resp.json()
    assert data["check"] == "db"
    assert "ok" in data
    assert "time" in data
