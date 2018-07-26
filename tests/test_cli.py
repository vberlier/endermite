from importlib.resources import read_binary
import pytest
from click.testing import CliRunner

import endermite
from endermite.cli import ender
from endermite.cli.config import ENDERMITE_FOLDER_PATH, LEVEL_DATA_PATH


@pytest.fixture
def runner():
    return CliRunner()


def test_version_flag(runner):
    result = runner.invoke(ender, ['--version'])
    assert result.exit_code == 0
    assert endermite.__version__ in result.output


class TestInitCommand:
    def test_empty_directory(self, runner):
        with runner.isolated_filesystem():
            result = runner.invoke(ender, ['init'])
            assert result.exit_code == 1
            assert 'Couldn\'t find any "level.dat" file' in result.output

    def test_invalid_level_dat(self, runner):
        with runner.isolated_filesystem():
            LEVEL_DATA_PATH.write_bytes(b'random stuff')

            result = runner.invoke(ender, ['init'])
            assert result.exit_code == 1
            assert 'Couldn\'t load level data' in result.output

    def test_old_world(self, runner):
        with runner.isolated_filesystem():
            LEVEL_DATA_PATH.write_bytes(read_binary('tests.files', 'old_level.dat'))

            result = runner.invoke(ender, ['init'])
            assert result.exit_code == 1
            assert 'not compatible with endermite' in result.output

    def test_command_result(self, runner):
        with runner.isolated_filesystem():
            LEVEL_DATA_PATH.write_bytes(read_binary('tests.files', 'level.dat'))

            result = runner.invoke(ender, ['init'], input='something\n\n\n\n\n')
            assert result.exit_code == 0
            assert ENDERMITE_FOLDER_PATH.is_dir()

            project_path = ENDERMITE_FOLDER_PATH / 'something'
            assert project_path.is_dir()
