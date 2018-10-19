import logging


def validate_parameters(parameters):

    valid = True

    if 'Environment' not in parameters:
        logging.error('Missing Environment in Parameters')
        valid = False
    if 'Brand' not in parameters:
        logging.error('Missing Brand in Parameters')
        valid = False
    if 'Application' not in parameters:
        logging.error('Missing Application in Parameters')
        valid = False
    if 'Owner' not in parameters:
        logging.error('Missing Owner in Parameters')
        valid = False

    return valid


def generate_stack_name(parameters):
    return f"{parameters['Environment']}-{parameters['Brand']}-{parameters['Application']}"


def merge_tags(tags, parameters):

    tags['Environment'] = merge_tag(tags, 'Environment', parameters['Environment'])
    tags['BusinessUnit'] = merge_tag(tags, 'BusinessUnit', parameters['Brand'])
    tags['Application'] = merge_tag(tags, 'Application', parameters['Application'])
    tags['Owner'] = merge_tag(tags, 'Owner', parameters['Owner'])
    tags['Name'] = merge_tag(tags, 'Name', generate_stack_name(parameters))

    logging.info('Merged Tags: %s', tags)
    return tags


def merge_tag(tags, tag_name, desired_value):

    current_value = tags.get(tag_name, None)

    if current_value not in (None, desired_value):
        logging.warning('%s tag does not conform to the Tagging Policy and will be overwritten', tag_name)

    return desired_value

def display_generated_values(parameters):
    print('')
    print('Stack Name:', generate_stack_name(parameters))
