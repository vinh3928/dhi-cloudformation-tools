from ..utils import aws
from ..utils import utils
from ..services.cloudformation import validate_template, package_template, deploy_template


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'package',
        aliases=['pkg'],
        help='Validates and Packages the specified AWS CloudFormation template.'
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
    parser.add_argument(
        '--s3-bucket',
        '-b',
        help='The name of the S3 bucket where this command uploads the artifacts that are referenced in your template.'
    )
    parser.add_argument(
        '--kms-key-id',
        '-k',
        help='The ID of an AWS KMS key that the command uses to encrypt artifacts that are at rest in the S3 bucket.'
    )
    parser.set_defaults(subcommand=main)


def main(args):

    session = aws.get_session(args.profile)
    aws.display_session_info(session)

    if not args.profile:
        utils.get_confirmation()

    validate_template(
        session,
        args
    )

    package_template(
        session,
        args
    )
