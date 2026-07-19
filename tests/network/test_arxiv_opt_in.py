import os

import pytest


@pytest.mark.skipif(os.getenv("ENABLE_NETWORK_TESTS") != "1", reason="network tests are opt-in")
def test_network_tests_are_opt_in() -> None:
    assert os.getenv("ENABLE_NETWORK_TESTS") == "1"
