import argparse

def common():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--profile',
        '-p',
        help='aws profile'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose mode.'
    )
    return parser


def template_config():
    parser = argparse.ArgumentParser(
        add_help=False,
        conflict_handler='resolve'
    )
    parser.add_argument(
        '--template',
        '-t',
        help='The path where your AWS CloudFormation template is located. (default: main.yml)',
        default='main.yml'
    )
    parser.add_argument(
        '--config',
        '-c',
        help='The path where your AWS CloudFormation template configuration is located. (default: config.json)',
        default='config.json'
    )
    return parser


def package_destination():
    parser = argparse.ArgumentParser(
        add_help=False,
        conflict_handler='resolve'
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
    return parser


def stackname_group():
    parent_parser = argparse.ArgumentParser(
        add_help=False,
        conflict_handler='resolve'
    )
    group = parent_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--config',
        '-c',
        help='The path where your AWS CloudFormation template configuration is located.',
    )
    group.add_argument(
        '--stack-name',
        help='The stack name to describe.',
    )
    return group


def approve():
    parser = argparse.ArgumentParser(
        add_help=False,
        conflict_handler='resolve'
    )
    parser.add_argument(
        '--approve',
        '-a',
        action='store_true',
        help='Approve command execution and bypass manual confirmation',
    )
    return parser
