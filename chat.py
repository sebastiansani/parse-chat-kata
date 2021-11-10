"""
Function that parses a chat string to the correct format.

Given the input

14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

The output should be

[{
  date: '14:24:32',
  mention: '14:24:32 Customer : ',
  sentence: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
  type: 'customer'
}]
"""

import re


def chat_parser(chat):
    if chat is None or chat == '':
        return []
    parsed_chat = []
    if '\n' in chat:
        split_chat = chat.splitlines(True)
    else:
        split_chat_with_separators = re.split(
            r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9])', chat)
        split_chat = [split_chat_with_separators[i] + split_chat_with_separators[i+1] for i in range(1, len(split_chat_with_separators)-1, 2)]
    for line in split_chat:
        parsed_line = line_parser(line)
        parsed_chat.append(parsed_line)
    return parsed_chat


def line_parser(line):
    parsed_line = {}
    split_line = line.split(' ')
    parsed_line['date'] = split_line[0]
    parsed_line['mention'] = split_line[0] + ' ' + split_line[1] + ' : '
    parsed_line['sentence'] = ' '.join(split_line[3:])
    parsed_line['type'] = split_line[1].lower()
    return parsed_line
