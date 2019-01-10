from termcolor import colored
from ..utils import aws, conventions
from ..services import cloudformation
from . import options

SECTIONS = ['outputs', 'parameters', 'status']


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'describe',
        parents=[
            options.common(),
            options.stackname_group()
        ],
        help='Describes details of a stack (outputs, resources, etc)',
    )
    parser.add_argument(
        '--sections',
        help=f'Which stack sections to display.  Accepts one or more of the following: {", ".join(SECTIONS)}, all (default: all)',
        nargs='*',
        default='all'
    )
    parser.set_defaults(subcommand=main)


def main(args):
    if 'stack_name' not in args and 'config' not in args:
        print('error: one of the arguments --config/-c --stack-name is required')

    if 'all' in args.sections:
        sections = SECTIONS
    else:
        sections = args.sections

    session = aws.get_session(args.profile)
    aws.display_session_info(session)

    if args.config:
        config = cloudformation.get_config(args.config)
        conventions.display_generated_values(config)
        stack_name = conventions.generate_stack_name(config['Parameters'])
    else:
        stack_name = args.stack_name

    print('Stack: ', colored(stack_name, 'green'))
    print('\nGetting stack details ...')
    stack_details = cloudformation.get_stack_details(session, stack_name)
    if stack_details:
        print('Stack: ', colored(stack_name, 'green'))
        if 'status' in sections:
            aws.display_cfn_stack_status(stack_details)
        if 'parameters' in sections:
            aws.display_cfn_stack_parameters(stack_details)
        if 'outputs' in sections:
            aws.display_cfn_stack_outputs(stack_details)
