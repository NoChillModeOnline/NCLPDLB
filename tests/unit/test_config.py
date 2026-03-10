"""Tests for src/config.py — Settings properties."""
import pytest
from src.config import Settings


@pytest.fixture
def base_settings():
    """A Settings instance with required fields filled in; reads rest from .env."""
    return Settings()


def test_cors_origins_list_single(base_settings):
    base_settings.cors_origins = "http://localhost:5173"
    assert base_settings.cors_origins_list == ["http://localhost:5173"]


def test_cors_origins_list_multiple(base_settings):
    base_settings.cors_origins = "http://localhost:5173,http://localhost:3000"
    result = base_settings.cors_origins_list
    assert "http://localhost:5173" in result
    assert "http://localhost:3000" in result
    assert len(result) == 2


def test_cors_origins_list_trims_whitespace(base_settings):
    base_settings.cors_origins = " http://a.com , http://b.com "
    result = base_settings.cors_origins_list
    assert "http://a.com" in result
    assert "http://b.com" in result


def test_video_storage_backend_free(base_settings):
    base_settings.deploy_target = "free"
    assert base_settings.video_storage_backend == "r2"


def test_video_storage_backend_azure(base_settings):
    base_settings.deploy_target = "azure"
    assert base_settings.video_storage_backend == "azure"
