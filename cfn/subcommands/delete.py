from termcolor import colored
from ..utils import aws, conventions
from ..services import cloudformation
from . import options


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'delete',
        parents=[
            options.common(),
            options.stackname_group()
        ],
        help='Deletes an existing stack',
    )
    parser.set_defaults(subcommand=main)


def main(args):
    if 'stack_name' not in args and 'config' not in args:
        print('error: one of the arguments --config/-c --stack-name is required')

    session = aws.get_session(args.profile)
    aws.display_session_info(session)

    if args.config:
        config = cloudformation.get_config(args.config)
        conventions.display_generated_values(config)
        stack_name = conventions.generate_stack_name(config['Parameters'])
    else:
        stack_name = args.stack_name

    print('Stack: ', colored(stack_name, 'green'))
    print('\nDeleting stack ...')
    cloudformation.delete_stack(session, stack_name)
