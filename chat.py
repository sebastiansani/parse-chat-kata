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
            r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w\s]+ :)|([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w]+ )', chat)
        split_chat_with_separators = [x for x in split_chat_with_separators if x != '' and x != None]
        split_chat = [split_chat_with_separators[i] + split_chat_with_separators[i+1] for i in range(0, len(split_chat_with_separators)-1, 2)]
    customer_name_match_obj = re.search(r"([0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([\w\s]+) :)|([0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([\w]+) )", split_chat[0])
    customer_name = customer_name_match_obj.group(2) if customer_name_match_obj.group(1) != None else customer_name_match_obj.group(4)
    for line in split_chat:
        parsed_line = line_parser(line, customer_name)
        parsed_chat.append(parsed_line)
    return parsed_chat


def line_parser(line, customer_name):
    parsed_line = {}
    match_obj = re.search(r"((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w\s]+) : )(.+\n*))|((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w]+) )(.+\n*))", line)
    i = 0 if match_obj.group(1) != None else 5
    parsed_line['date'] = match_obj.group(3+i)
    parsed_line['mention'] = match_obj.group(2+i)
    parsed_line['sentence'] = match_obj.group(5+i)
    parsed_line['type'] = 'customer' if match_obj.group(4+i) == customer_name else 'agent'
    return parsed_line
