from typing import Literal

import pytest


Operator = Literal["+", "-"]


@pytest.fixture
def ensure_logging():
    from ui.logger import init_logging

    init_logging()
