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

    print('\nValidating...')
    client = session.create_client('cloudformation')
    template_body = utils.read_content(args.template)
    config = utils.read_json(args.config)

    if not validate_template_config(config):
        logging.error('Invalid template config.')
        sys.exit(1)
    print('The config is valid.')

    try:
        client.validate_template(
            TemplateBody=template_body,
        )
    except botocore.exceptions.ClientError as ex:
        logging.error(ex)
        sys.exit(1)

    print('The template is valid.')
    return config['Parameters']


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
    s3_prefix = args.s3_prefix or conventions.generate_stack_name(config['Parameters'])

    try:
        s3_uploader = S3Uploader(
            client,
            args.s3_bucket,
            session.get_scoped_config()['region'],
            s3_prefix,
            args.kms_key_id,
            False
        )
        template = Template(args.template, os.getcwd(), s3_uploader)
        exported_template = template.export()
        exported_template_yaml = yaml_dump(exported_template)
    except exceptions.ExportFailedError as ex:
        if template_has_resources_to_export(template) and not args.s3_bucket:
            logging.error('The template contains resources to export, please provide an S3 Bucket (--s3-prefix).')
        else:
            logging.error(ex)
        sys.exit(1)

    logging.info(exported_template_yaml)
    print('Done.')
    return exported_template_yaml


def template_has_resources_to_export(template):
    if "Resources" in template.template_dict:
        for _, resource in template.template_dict["Resources"].items():
            resource_type = resource.get("Type", None)
            for exporter_class in template.resources_to_export:
                if exporter_class.RESOURCE_TYPE == resource_type:
                    return True
    return False


def deploy_template(session, args, packaged_yaml):

    print('\nDeploying...')
    client = session.create_client('cloudformation')
    config = utils.read_json(args.config)
    stack_name = conventions.generate_stack_name(config['Parameters'])
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
