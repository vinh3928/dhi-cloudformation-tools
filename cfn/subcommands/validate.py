from ..utils import aws
from ..utils import utils
from ..services.cloudformation import validate_template


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'validate',
        aliases=['val'],
        help='Validates the specified AWS CloudFormation template.'
    )
    parser.add_argument(
        '--profile',
        '-p',
        help='aws profile'
    )
    parser.add_argument(
        '--template',
        '-t',
        help='The path where your AWS CloudFormation template is located.',
        default='main.yml'
    )
    parser.add_argument(
        '--config',
        '-c',
        help='The path where your AWS CloudFormation template configuration is located.',
        default='config.json'
    )
    parser.set_defaults(subcommand=main)


def main(args):

    session = aws.get_session(args.profile)

    aws.display_session_info(session)

    validate_template(
        session,
        args
    )
