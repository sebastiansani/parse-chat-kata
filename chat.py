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
            r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [A-Za-z\s]+ :)', chat)
        split_chat = [split_chat_with_separators[i] + split_chat_with_separators[i+1] for i in range(1, len(split_chat_with_separators)-1, 2)]
    customer_name = re.search(r"^[0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([A-Za-z\s]+) :", split_chat[0]).group(1)
    for line in split_chat:
        parsed_line = line_parser(line, customer_name)
        parsed_chat.append(parsed_line)
    return parsed_chat


def line_parser(line, customer_name):
    parsed_line = {}
    match_obj = re.search(r"^(([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([A-Za-z\s]+) : )(.+\n*)", line)
    parsed_line['date'] = match_obj.group(2)
    parsed_line['mention'] = match_obj.group(1)
    parsed_line['sentence'] = match_obj.group(4)
    parsed_line['type'] = 'customer' if match_obj.group(3) == customer_name else 'agent'
    return parsed_line
