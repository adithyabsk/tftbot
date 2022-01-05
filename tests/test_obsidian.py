"""Test Obsidian block query integration."""

import os

import pytest

RUN_INTEGRATION = bool(os.getenv("INTEGRATION", False))


@pytest.mark.skipif(
    not RUN_INTEGRATION,
    reason="Requires obsidian env vars to be set.",
)
def test_integration_obsidian_query():
    """Test Obsidian random block query."""
    from dotenv import load_dotenv

    from tftbot.obsidian import get_all_tag_blocks

    load_dotenv("../.env")

    obsidian_tag = os.environ["TAG"]
    blocks = get_all_tag_blocks(obsidian_tag)

    # Check to make sure that the blocks are not empty
    assert len(blocks) > 0
