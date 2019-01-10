import os
import sys
import logging
import json
import botocore
from termcolor import colored
from prettytable import PrettyTable, prettytable
from . import utils

DEFAULT_COLOR = 'white'
STATUS_COLORS = {
    'CREATE_IN_PROGRESS': 'blue',
    'CREATE_FAILED': 'red',
    'CREATE_COMPLETE': 'green',
    'ROLLBACK_IN_PROGRESS': 'yellow',
    'ROLLBACK_FAILED': 'red',
    'ROLLBACK_COMPLETE': 'yellow',
    'DELETE_IN_PROGRESS': 'blue',
    'DELETE_FAILED': 'red',
    'DELETE_COMPLETE': 'green',
    'UPDATE_IN_PROGRESS': 'blue',
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS': 'blue',
    'UPDATE_COMPLETE': 'green',
    'UPDATE_FAILED': 'red',
    'UPDATE_ROLLBACK_IN_PROGRESS': 'red',
    'UPDATE_ROLLBACK_FAILED': 'red',
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS': 'yellow',
    'UPDATE_ROLLBACK_COMPLETE': 'yellow',
    'REVIEW_IN_PROGRESS': 'blue'
}

ACTION_COLORS = {
    'Add': 'green',
    'Modify': 'yellow',
    'Remove': 'red'
}

REPLACEMENT_COLORS = {
    'True': 'red',
    'False': 'green'
}

def get_session(profile):
    return botocore.session.Session(profile=profile)


def get_region(session):
    return session.get_scoped_config().get('region') or os.environ.get('AWS_DEFAULT_REGION')


def display_session_info(session):
    try:
        print('')
        profile = 'default' if not session.profile else session.profile
        print('Profile:', colored(profile, 'green')
              or colored('default', 'yellow'))
        print('Region:', colored(
            session.get_scoped_config().get('region', 'n/a'), 'green'))
        print('AWS Account Number:', colored(
            session.get_scoped_config().get('aws_account_number', 'n/a'), 'green'))
    except botocore.exceptions.ProfileNotFound as ex:
        logging.error(ex)
        sys.exit(1)


def display_cfn_stack_outputs(stack_details):
    if 'Outputs' in stack_details and stack_details['Outputs']:
        outputs = stack_details['Outputs']
        outputs_table = PrettyTable(
            title=colored('Stack Outputs', 'green'),
            hrules=prettytable.ALL,
            align='l',
            field_names=[
                'OutputKey',
                'Description',
                'OutputValue',
                'ExportName'
            ],
            sortby='OutputKey'
        )

        for output in outputs:
            outputs_table.add_row([
                output.get('OutputKey', ''),
                output.get('Description', ''),
                output.get('OutputValue', ''),
                output.get('ExportName', ''),
            ])

        print(outputs_table)


def display_cfn_stack_status(stack_details):
    print('Status: ', colored(stack_details['StackStatus'], STATUS_COLORS[stack_details['StackStatus']]))


def display_cfn_stack_parameters(stack_details):
    if 'Parameters' in stack_details and stack_details['Parameters']:
        parameters = stack_details['Parameters']
        table = PrettyTable(
            title=colored('Stack Parameters', 'green'),
            hrules=prettytable.ALL,
            align='l',
            field_names=[
                'Key',
                'Value',
            ],
            sortby='Key'
        )

        for parameter in parameters:
            table.add_row([
                parameter.get('ParameterKey', ''),
                parameter.get('ParameterValue', ''),
            ])

        print(table)


def display_cfn_stack_events(events):
    field_names = [
        'Timestamp (UTC)',
        'ResourceStatus',
        'ResourceType',
        'LogicalResourceId',
        'PhysicalResourceId',
        'ResourceStatusReason',
    ]
    table = PrettyTable(
        title=colored('Stack Events', 'green'),
        hrules=prettytable.ALL,
        align='l',
        field_names=field_names,
    )

    for event in events:
        event_status = event.get('ResourceStatus', '')
        row_color = STATUS_COLORS.get(event_status, 'white')
        physical_id_formatted = utils.wrap_text(event.get('PhysicalResourceId', ''), 25, row_color)
        status_reason_formatted = utils.wrap_text(event.get('ResourceStatusReason', ''), 40, row_color)
        formatted_timestamp = event['Timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        table.add_row([
            colored(formatted_timestamp, row_color),
            colored(event_status, row_color),
            colored(event.get('ResourceType', ''), row_color),
            colored(event.get('LogicalResourceId', ''), row_color),
            physical_id_formatted,
            status_reason_formatted,
        ])

    print(table)


def display_cfn_changeset(changeset_changes):
    table = PrettyTable(
        title=colored('Stack Changes', 'green'),
        hrules=prettytable.ALL,
        field_names=[
            'Action',
            'LogicalResourceId',
            'PhysicalResourceId',
            'ResourceType',
            'Replacement',
            'Scope',
            'Details'
        ],
        sortby='Action'
    )

    table.align['Details'] = "l"
    table.align['PhysicalResourceId'] = "l"
    for change in changeset_changes:
        resource_change = change['ResourceChange']
        action = resource_change.get('Action', '')
        replacement = resource_change.get('Replacement', '')
        action_color = ACTION_COLORS.get(action, DEFAULT_COLOR)
        replacement_color = REPLACEMENT_COLORS.get(replacement, DEFAULT_COLOR)
        details = json.dumps(resource_change.get('Details', ''), indent=2)
        details = details.replace(
            'CausingEntity', colored('CausingEntity', 'yellow'))
        details = details.replace('"Name"', colored('"Name"', 'green'))
        physical_id = resource_change.get(
            'PhysicalResourceId', '').replace('/', '\n  /')
        record = [
            colored(action, action_color),
            resource_change.get('LogicalResourceId', ''),
            physical_id,
            resource_change.get('ResourceType', ''),
            colored(replacement, replacement_color),
            resource_change.get('Scope', ''),
            details
        ]
        table.add_row(record)

    print(table)
