
import pytest
from pydantic import ValidationError

from src.chunking.config import ChunkingConfig


def test_default_config_is_valid():
    config = ChunkingConfig()

    assert config.child_chunk_size == 500
    assert config.child_chunk_overlap == 60
    assert config.parent_chunk_size == 1500
    assert config.chunking_version == "v1"


def test_overlap_must_be_smaller_than_child_size():
    with pytest.raises(ValidationError):
        ChunkingConfig(
            child_chunk_size=100,
            child_chunk_overlap=100,
        )


def test_parent_must_be_at_least_child_size():
    with pytest.raises(ValidationError):
        ChunkingConfig(
            child_chunk_size=500,
            parent_chunk_size=300,
        )


def test_unknown_settings_are_rejected():
    with pytest.raises(ValidationError):
        ChunkingConfig(unexpected_setting=123)


def test_config_is_immutable():
    config = ChunkingConfig()

    with pytest.raises(ValidationError):
        config.child_chunk_size = 800
