from ..utils import aws, utils, conventions
from ..services.cloudformation import validate_template, package_template


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
        '--s3-prefix',
        '-pf',
        help='A prefix name that the command adds to the artifact\'s name when it uploads them to the S3 bucket.'
    )
    parser.add_argument(
        '--kms-key-id',
        '-k',
        help='The ID of an AWS KMS key that the command uses to encrypt artifacts that are at rest in the S3 bucket.'
    )
    parser.add_argument(
        '--output-template-file',
        '-o',
        help='The path to the file where the command writes the output AWS CloudFormation template.',
        default='packaged.yml'
    )
    parser.add_argument(
        '--approve',
        '-a',
        action='store_true',
        help='Approve command execution and bypass manual confirmation.',
    )
    parser.set_defaults(subcommand=main)


def main(args):

    session = aws.get_session(args.profile)

    aws.display_session_info(session)

    valid_parameters = validate_template(
        session,
        args
    )

    conventions.display_generated_values(valid_parameters)

    if not args.approve:
        utils.get_confirmation()

    packaged_yaml = package_template(
        session,
        args
    )

    utils.write_content(args.output_template_file, packaged_yaml)
