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


class ChatParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_chat(chat):
        if chat is None or chat == '':
            return []
        parsed_chat = []
        if '\n' in chat:
            split_chat = chat.splitlines(True)
        else:
            split_chat = ChatParser.split_dates(chat)
        customer_name = ChatParser.get_customer_name(split_chat[0])
        for line in split_chat:
            parsed_line = ChatParser.parse_line(line, customer_name)
            parsed_chat.append(parsed_line)
        return parsed_chat

    @staticmethod
    def parse_line(line, customer_name):
        parsed_line = {}
        line_elements = ChatParser.get_line_elements(line)
        parsed_line['mention'] = line_elements[1]
        parsed_line['date'] = line_elements[2]
        parsed_line['type'] = 'customer' if line_elements[3] == customer_name else 'agent'
        parsed_line['sentence'] = line_elements[4]
        return parsed_line

    @staticmethod
    def get_line_elements(line):
        line_regex = r"((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w\s]+) : )(.+\n*))|((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w]+) )(.+\n*))"
        line_elements = re.search(line_regex, line)
        clean_line_elements = [x for x in line_elements.groups() if x !=
                               '' and x != None]
        return clean_line_elements

    @staticmethod
    def split_dates(chat):
        date_splitter_regex = r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w\s]+ :)|([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w]+ )'
        split_chat_with_separators = re.split(date_splitter_regex, chat)
        clean_split_chat_with_separators = [
            x for x in split_chat_with_separators if x != '' and x != None]
        split_chat = [clean_split_chat_with_separators[i] + clean_split_chat_with_separators[i+1]
                      for i in range(0, len(clean_split_chat_with_separators)-1, 2)]
        return split_chat

    @staticmethod
    def get_customer_name(customer_line):
        customer_name_regex = r"([0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([\w\s]+) :)|([0-9][0-9]:[0-9][0-9]:[0-9][0-9] ([\w]+) )"
        customer_name_match_obj = re.search(customer_name_regex, customer_line)
        customer_name = [x for x in customer_name_match_obj.groups()
                         if x != '' and x != None][1]
        return customer_name
