from toolbox import cli


def version():
    cli.echo("0.0.16")


class CommandVersion:
    name = "version"
    help = "Shows current version"
    handler = version
