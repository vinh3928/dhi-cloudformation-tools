from ..utils import aws
from ..services.cloudformation import validate_template, get_template, get_config


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
        help='The path where your AWS CloudFormation template is located. (default: main.yml)',
        default='main.yml'
    )
    parser.add_argument(
        '--config',
        '-c',
        help='The path where your AWS CloudFormation template configuration is located. (default: config.json)',
        default='config.json'
    )
    parser.set_defaults(subcommand=main)


def main(args):

    session = aws.get_session(args.profile)

    aws.display_session_info(session)

    template = get_template(args.template)
    config = get_config(args.config)

    validate_template(
        session,
        template,
        config
    )
