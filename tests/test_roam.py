"""Tests for roam graph queries."""

import os

import pytest

RUN_INTEGRATION = bool(os.getenv("INTEGRATION", False))


@pytest.mark.skipif(
    not RUN_INTEGRATION,
    reason=(
        "Requires roam-api to be installed and env vars to be configured. "
        "Runs for around 9s"
    ),
)
def test_integration_roam_query():
    """Test Roam graph queries.

    Make sure that the [[TAG]] specified in env vars exists in the graph.

    """
    from dotenv import load_dotenv

    from tftbot.roam import block_search

    load_dotenv("../.env")

    roam_tag = os.environ["TAG"]
    roam_api_graph = os.environ["ROAM_API_GRAPH"]
    roam_api_email = os.environ["ROAM_API_EMAIL"]
    roam_api_password = os.environ["ROAM_API_PASSWORD"]

    blocks = block_search(roam_tag, roam_api_graph, roam_api_email, roam_api_password)

    # Check to make sure that the blocks are not empty
    assert len(blocks) > 0
