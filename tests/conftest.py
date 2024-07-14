from pathlib import Path
import pytest


@pytest.fixture
def sample_1_html():
    sample = Path(__file__).parent / "data/sample-1.html"
    return sample.read_text()


@pytest.fixture
def sample_2_html():
    sample = Path(__file__).parent / "data/sample-2.html"
    return sample.read_text()
