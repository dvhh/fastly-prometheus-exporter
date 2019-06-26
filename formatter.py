'''
Create format report from json to html using jinja2
'''
import json
import sys
import argparse
from jinja2 import Template


def get_template(argument: str):
    '''
    get template content
    '''
    if argument == '-':
        return Template(sys.stdin.read())
    return Template(open(argument).read())


def get_entries(argument: str):
    '''
    get stream for reading json file
    '''
    if argument == '-':
        return sys.stdin
    return open(argument, mode='rt')


def main():
    '''
    Main entry point
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        help='file containing result of comparison,' +
        ' use \'-\' for stdin (default)',
        metavar=('<name>', '<file>'),
        nargs=2,
        action='append'
    )
    parser.add_argument(
        '-t',
        '--template',
        help='file containing template' +
        ', use \'-\' for stdin (default:\'metrics.jinja.txt\')',
        metavar='<template file>',
        default='metrics.jinja.txt'
    )
    args = parser.parse_args()

    # Verify args
    assert(args.input is not None), 'please specify at least one input'

    use_stdin = len(list(filter(lambda value: value[0] == '-', args.input)))
    if args.template == '-':
        use_stdin += 1
    assert use_stdin <= 1, 'stdin used multiple times'
    template = get_template(args.template)
    template_args = {}

    for pair in args.input:
        template_args[pair[0]] = json.load(get_entries(pair[1]))

    print(template.render(**template_args))


if __name__ == '__main__':
    main()
