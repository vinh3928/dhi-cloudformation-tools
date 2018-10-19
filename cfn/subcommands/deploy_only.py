from ..utils import aws, utils, conventions
from ..services.cloudformation import validate_template, package_template, deploy_template, get_config_parameters


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'deploy-only',
        aliases=['dplo'],
        help='Deploys the specified AWS CloudFormation template by creating and then executing a change set.'
    )
    parser.add_argument(
        '--profile',
        '-p',
        help='aws profile'
    )
    parser.add_argument(
        '--packaged',
        '-k',
        help='The path where your AWS CloudFormation packaged template is located.',
        default='packaged.yml'
    )
    parser.add_argument(
        '--config',
        '-c',
        help='The path where your AWS CloudFormation template configuration is located.',
        default='config.json'
    )
    parser.add_argument(
        '--approve',
        '-a',
        action='store_true',
        help='Approve command execution and bypass manual confirmation',
    )
    parser.set_defaults(subcommand=main)


def main(args):

    session = aws.get_session(args.profile)

    aws.display_session_info(session)

    config_parameters = get_config_parameters(args)

    conventions.display_generated_values(config_parameters)

    packaged_yaml = utils.read_content(args.packaged)

    if not args.approve:
        utils.get_confirmation()

    deploy_template(
        session,
        args,
        packaged_yaml
    )
