import pytest

FOUNTAIN_SAMPLE = """DAVE
Hi Philip

PHILIP
Hello David

Dave and Philip stand in silence for three hours
"""


@pytest.fixture
def fountain_sample():
    return FOUNTAIN_SAMPLE
