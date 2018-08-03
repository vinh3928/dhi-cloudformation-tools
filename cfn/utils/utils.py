import sys
import logging
import json


def get_json(filepath):

    try:
        with open(filepath) as file:
            content = json.load(file)
    except FileNotFoundError as ex:
        logging.error(ex)
        sys.exit(1)
    except json.decoder.JSONDecodeError as ex:
        logging.error('Invalid json:%s', filepath)
        sys.exit(1)

    return content


def get_content(filepath):

    try:
        with open(filepath, "r") as file:
            content = file.read()
    except FileNotFoundError as ex:
        logging.error(ex)
        sys.exit(1)

    return content

def get_confirmation():
    response = input("Continue? (y/n)\n")
    if response != 'y':
        sys.exit(1)
