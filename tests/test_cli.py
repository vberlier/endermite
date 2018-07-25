import pytest
from click.testing import CliRunner

import endermite
from endermite.cli import ender


@pytest.fixture
def runner():
    return CliRunner()


def test_version_flag(runner):
    result = runner.invoke(ender, ['--version'])
    assert result.exit_code == 0
    assert endermite.__version__ in result.output
