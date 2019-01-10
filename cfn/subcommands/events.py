from datetime import datetime, timedelta, timezone


from termcolor import colored
from ..utils import aws, conventions
from ..services import cloudformation
from . import options

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'events',
        parents=[
            options.common(),
            options.stackname_group()
        ],
        help='Get stack events'
    )
    parser.add_argument(
        '--filter-minutes',
        help='The number of minutes to filter events. (default: 5)',
        default=5,
        type=int
    )

    parser.set_defaults(subcommand=main)


def main(args):
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
    filter_time = datetime.now(timezone.utc) - timedelta(hours=0, minutes=args.filter_minutes)

    stack_events = cloudformation.get_stack_events(session, stack_name, since=filter_time)
    if stack_events:
        print('Stack: ', colored(stack_name, 'green'))
        aws.display_cfn_stack_events(stack_events)
    else:
        print('Error: no events matching filter')
