"""Sample CLI test."""

from click.testing import CliRunner

from idact.notebook import main


def test_no_cluster_name():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    print(result.output)
    assert 'Usage: main [OPTIONS] CLUSTER_NAME\n' in result.output
    assert 'Error: Missing argument' in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    print(result.output)
    assert 'A console script that executes a Jupyter Notebook instance' \
           in result.output
    assert 'Show this message and exit.' in result.output
