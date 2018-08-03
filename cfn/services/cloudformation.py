import os
import sys
import logging
import botocore.exceptions
from awscli.customizations.cloudformation.artifact_exporter import Template
from awscli.customizations.cloudformation.deployer import Deployer
from awscli.customizations.s3uploader import S3Uploader
from awscli.customizations.cloudformation.yamlhelper import yaml_dump
from awscli.customizations.cloudformation import exceptions
from ..utils import utils, conventions


def validate_template(session, args):

    print('Validating...')
    client = session.create_client('cloudformation')
    template_body = utils.get_content(args.template)
    config = utils.get_json(args.config)

    if not validate_template_config(config):
        logging.error('Invalid template config.')
        sys.exit(1)
    print('The template config is valid.')

    try:
        client.validate_template(
            TemplateBody=template_body,
        )
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        sys.exit(1)

    print('The template is valid.')

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

    print('Packaging...')
    client = session.create_client('s3')
    config = utils.get_json(args.config)

    try:
        s3_uploader = S3Uploader(
            client,
            args.s3_bucket,
            session.get_scoped_config()['region'],
            conventions.generate_name(config['Parameters']),
            args.kms_key_id,
            False
        )
        template = Template(args.template, os.getcwd(), s3_uploader)
        exported_template = template.export()
        exported_template_yaml = yaml_dump(exported_template)
    except exceptions.ExportFailedError as ex:
        logging.error(ex)
        sys.exit(1)

    logging.info(exported_template_yaml)
    print('Done.')
    return exported_template_yaml


def deploy_template(session, args, packaged_yaml):

    print('Deploying...')
    client = session.create_client('cloudformation')
    config = utils.get_json(args.config)
    stack_name = conventions.generate_name(config['Parameters'])
    deployer = Deployer(client)
    tags = conventions.merge_tags(config.get('Tags', {}), config['Parameters'])

    try:
        result = deployer.create_and_wait_for_changeset(
            stack_name=stack_name,
            cfn_template=packaged_yaml,
            parameter_values=deploy_template_parameters_builder(config['Parameters']),
            capabilities=['CAPABILITY_NAMED_IAM'],
            role_arn=None,
            notification_arns=None,
            s3_uploader=None,
            tags=deploy_template_tags_builder(tags)
        )
        deployer.execute_changeset(result.changeset_id, stack_name)
        deployer.wait_for_execute(stack_name, result.changeset_type)
    except exceptions.ChangeEmptyError as ex:
        logging.error(ex)
        sys.exit(1)
    except exceptions.DeployFailedError as ex:
        logging.error(ex)
        sys.exit(1)
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        sys.exit(1)

    print('Done.')


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
