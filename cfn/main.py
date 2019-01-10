import logging
import argparse
import coloredlogs
import colorama
from . import version
from .subcommands import validate, package, deploy, deploy_only, describe, options, events, delete


def init_parser():
    parser = argparse.ArgumentParser(
        prog='cfn',
        description=f'DHI CloudFormation Tools {version.__version__}',
        conflict_handler='resolve',
        parents=[options.common()]
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'DHI CloudFormation Tools {version.__version__}'
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
    )
    validate.add_subparser(subparsers)
    package.add_subparser(subparsers)
    deploy.add_subparser(subparsers)
    deploy_only.add_subparser(subparsers)
    describe.add_subparser(subparsers)
    events.add_subparser(subparsers)
    delete.add_subparser(subparsers)

    return parser


def invoke_subcommand(args):
    args.subcommand(args)


def main():

    parser = init_parser()
    args = parser.parse_args()
    coloredlogs.install(
        fmt='%(levelname)s:%(message)s',
        level=logging.INFO if args.verbose else logging.WARNING
    )

    invoke_subcommand(args)


if __name__ == '__main__':
    colorama.init()
    main()
