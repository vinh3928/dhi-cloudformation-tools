import sys
import logging
import json
import textwrap
from termcolor import colored

def read_json(filepath):
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


def read_content(filepath):
    try:
        with open(filepath, "r") as file:
            content = file.read()
    except FileNotFoundError as ex:
        logging.error(ex)
        sys.exit(1)

    return content


def write_content(filepath, content):
    with open(filepath, "w") as file:
        file.write(content)


def get_confirmation():
    response = input(colored("\nContinue? (y/n)\n", 'yellow'))
    if response != 'y':
        sys.exit(1)


def wrap_text(text, max_line_length, color='white'):
    wrapped_lines = textwrap.wrap(text, max_line_length)
    colored_lines = [colored(line, color) for line in wrapped_lines]
    return '\n'.join(colored_lines)
