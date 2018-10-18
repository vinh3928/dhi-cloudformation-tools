import logging
import argparse
from . import version
from .subcommands import validate, package, deploy


def init_parser():
    parser = argparse.ArgumentParser(
        prog='cfn',
        description=f'DHI CloudFormation Tools {version.__version__}'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'DHI CloudFormation Tools {version.__version__}'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='debug mode'
    )
    subparsers = parser.add_subparsers(help='available subcommands')
    validate.add_subparser(subparsers)
    package.add_subparser(subparsers)
    deploy.add_subparser(subparsers)
    return parser

def invoke_subcommand(args):
    args.subcommand(args)

def main():

    parser = init_parser()
    args = parser.parse_args()
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.INFO if args.verbose else logging.WARNING
    )

    try:
        invoke_subcommand(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
