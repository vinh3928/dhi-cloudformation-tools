from ..utils import aws, utils, conventions
from ..services.cloudformation import validate_template, package_template, get_template, get_config
from . import options

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'package',
        aliases=['pkg'],
        parents=[
            options.common(),
            options.template_config(),
            options.package_destination(),
            options.approve()
        ],
        help='Validates and Packages the specified AWS CloudFormation template.'
    )
    parser.add_argument(
        '--output-template-file',
        '-o',
        help='The path to the file where the command writes the output AWS CloudFormation template. (default: packaged.yml)',
        default='packaged.yml'
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

    conventions.display_generated_values(config)

    if not args.approve:
        utils.get_confirmation()

    packaged_yaml = package_template(
        session,
        args
    )

    utils.write_content(args.output_template_file, packaged_yaml)
