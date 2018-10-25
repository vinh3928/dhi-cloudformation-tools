import os
import sys
import logging
import botocore


def get_session(profile):
    return botocore.session.Session(profile=profile)


def get_region(session):
    return session.get_scoped_config().get('region') or os.environ.get('AWS_DEFAULT_REGION')


def display_session_info(session):
    try:
        print('')
        print('Profile:', session.profile or 'default')
        print('Region:', session.get_scoped_config().get('region', 'n/a'))
        print('AWS Account Number:', session.get_scoped_config().get('aws_account_number', 'n/a'))
    except botocore.exceptions.ProfileNotFound as ex:
        logging.error(ex)
        sys.exit(1)
