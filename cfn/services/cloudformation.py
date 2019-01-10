import os
import sys
import logging
import uuid
import datetime
import botocore.exceptions
from botocore.exceptions import ClientError
from termcolor import colored
from awscli.customizations.cloudformation.artifact_exporter import Template
from awscli.customizations.cloudformation.deployer import Deployer
from awscli.customizations.s3uploader import S3Uploader
from awscli.customizations.cloudformation.yamlhelper import yaml_dump
from awscli.customizations.cloudformation import exceptions
from ..utils import utils, aws, conventions




def validate_template(session, template, config):

    print('\nValidating...')
    client = session.create_client('cloudformation')

    if not validate_template_config(config):
        logging.error('Invalid template config.')
        sys.exit(1)
    print('The config is valid.')

    try:
        client.validate_template(
            TemplateBody=template,
        )
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        sys.exit(1)

    print('The template is valid.')


def get_config(config_filename):

    return utils.read_json(config_filename)


def get_template(template_filename):

    return utils.read_content(template_filename)


def validate_template_config(config):

    valid = True

    if 'Parameters' not in config:
        logging.error('Missing Parameters in config')
        valid = False
    elif not conventions.validate_parameters(config['Parameters']):
        logging.error('Invalid Parameters in config')
        valid = False

    return valid


def package_template(session, args):

    print('\nPackaging...')
    client = session.create_client('s3')
    config = utils.read_json(args.config)
    s3_prefix = args.s3_prefix or conventions.generate_stack_name(
        config['Parameters'])

    try:
        s3_uploader = S3Uploader(
            client,
            args.s3_bucket,
            aws.get_region(session),
            s3_prefix,
            args.kms_key_id,
            False
        )
        template = Template(args.template, os.getcwd(), s3_uploader)
        exported_template = template.export()
        exported_template_yaml = yaml_dump(exported_template)
    except exceptions.ExportFailedError as ex:
        if template_has_resources_to_upload_to_s3(template) and not args.s3_bucket:
            logging.error(
                'The template contains resources to upload, please provide an S3 Bucket (--s3-bucket).')
        else:
            logging.error(ex)
        sys.exit(1)

    logging.info(exported_template_yaml)
    print('Done.')
    return exported_template_yaml


def template_has_resources_to_upload_to_s3(template):
    """
    This function uses the aws cli provided class attribute 'Template.resources_to_export'
    that contains a static list of resource types
    to check if any of the resources in the template need to be uploaded to S3
    Reference: https://github.com/aws/aws-cli/blob/develop/awscli/customizations/cloudformation/artifact_exporter
    """

    if "Resources" in template.template_dict:
        for _, resource in template.template_dict["Resources"].items():
            resource_type = resource.get("Type", None)
            for exporter_class in template.resources_to_export:
                if exporter_class.RESOURCE_TYPE == resource_type:
                    return True
    return False


def get_changesetname_fromid(session, stack_name, changeset_id):
    client = session.create_client('cloudformation')
    response = client.list_change_sets(
        StackName=stack_name
    )
    for changeset in response['Summaries']:
        if changeset['ChangeSetId'] == changeset_id:
            return changeset['ChangeSetName']

    raise ValueError(
        f'no changeset with id {changeset_id} was found for stack {stack_name}')


def display_changeset(session, stack_name, changeset_id):
    client = session.create_client('cloudformation')
    changeset_name = get_changesetname_fromid(
        session, stack_name, changeset_id)
    response = client.describe_change_set(
        ChangeSetName=changeset_name,
        StackName=stack_name
    )
    changes = response['Changes']
    aws.display_cfn_changeset(changes)


def deploy_template(session, config, packaged_yaml, approve=False):
    success = True
    print('\nDeploying...')
    client = session.create_client('cloudformation')
    stack_name = conventions.generate_stack_name(config['Parameters'])
    deployer = Deployer(client)
    tags = conventions.merge_tags(config.get('Tags', {}), config['Parameters'])

    try:
        result = deployer.create_and_wait_for_changeset(
            stack_name=stack_name,
            cfn_template=packaged_yaml,
            parameter_values=deploy_template_parameters_builder(
                config['Parameters']),
            capabilities=['CAPABILITY_NAMED_IAM'],
            role_arn=None,
            notification_arns=None,
            s3_uploader=None,
            tags=deploy_template_tags_builder(tags)
        )
        display_changeset(session, stack_name, result.changeset_id)
        if not approve:
            utils.get_confirmation()

        execute_changeset_token = str(uuid.uuid4())
        client.execute_change_set(
            ChangeSetName=result.changeset_id,
            StackName=stack_name,
            ClientRequestToken=execute_changeset_token)
        deployer.wait_for_execute(stack_name, result.changeset_type)
    except exceptions.ChangeEmptyError as ex:
        logging.error(ex)
        success = False
    except exceptions.DeployFailedError as ex:
        logging.error(ex)
        # print(colored(ex.response['Error']['Message'], 'red'))
        stack_events = get_stack_events(
            session, stack_name, execute_changeset_token)
        aws.display_cfn_stack_events(stack_events)
        success = False
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        success = False

    print('Done.')
    return success


def deploy_template_parameters_builder(parameters):

    new_parameters = []

    for key, value in parameters.items():
        new_parameters.append({
            'ParameterKey': key,
            'ParameterValue': str(value)
        })

    return new_parameters


def deploy_template_tags_builder(tags):

    new_tags = []

    for key, value in tags.items():
        new_tags.append({
            'Key': key,
            'Value': value
        })

    return new_tags


def get_stack_details(session, stack_name):
    client = session.create_client('cloudformation')
    response = None
    try:
        response = client.describe_stacks(
            StackName=stack_name
        )
        if response['Stacks']:
            # Return the first stack as this is likely what we want
            return response['Stacks'][0]

    except ClientError as ex:
        print(colored('Error Getting Stack:', 'red'))
        print(colored(f"  {ex.response['Error']['Message']}", 'red'))

    return response


def get_stack_events(session, stack_name, client_request_token=None, since=None):
    print(colored('  getting events ...', 'yellow'))

    client = session.create_client('cloudformation')
    response = client.describe_stack_events(
        StackName=stack_name
    )

    events = []
    for event in response['StackEvents'] or []:
        # Filter events by client_request_token
        if client_request_token and event.get('ClientRequestToken', '') != client_request_token:
            continue

        # Filter events by timestamp
        if since and event.get('Timestamp', datetime.datetime(datetime.MINYEAR, 1, 1, tzinfo=datetime.timezone.utc)) <= since:
            continue

        # Any unfiltered events should be returned
        events.append(event)

    return events


def delete_stack(session, stack_name):
    client = session.create_client('cloudformation')

    try:
        client.delete_stack(
            StackName=stack_name
        )
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        sys.exit(1)

    print('The stack is deleting.')
