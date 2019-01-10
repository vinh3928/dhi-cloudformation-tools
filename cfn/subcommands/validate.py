from ..utils import aws
from ..services.cloudformation import validate_template, get_template, get_config
from . import options


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'validate',
        aliases=['val'],
        parents=[
            options.common(),
            options.template_config()
        ],
        help='Validates the specified AWS CloudFormation template.'
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
