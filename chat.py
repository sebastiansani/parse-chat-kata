"""
Function that parses a chat string to the correct format.

Given a list of chat messages as input:

    14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit.

The output is a list of dictionaries, each in the following format:

    [{
    date: '14:24:32',
    mention: '14:24:32 Customer : ',
    sentence: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    type: 'customer'
    },
    {
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
        """Parses the whole chat"""
        if chat is None or chat == '':
            return []
        parsed_chat = []
        if '\n' in chat:
            split_chat = chat.splitlines(True) # Split chat by newline and keep newline character
        else:
            split_chat = ChatParser.split_dates(chat) # Split chat by dates and keep dates
        customer_name = ChatParser.get_customer_name(split_chat[0])
        for line in split_chat:
            parsed_line = ChatParser.parse_line(line, customer_name)
            parsed_chat.append(parsed_line)
        return parsed_chat

    @staticmethod
    def parse_line(line, customer_name):
        """Parses a single line"""
        parsed_line = {}
        line_elements = ChatParser.get_line_elements(line)
        parsed_line['mention'] = line_elements[1]
        parsed_line['date'] = line_elements[2]
        parsed_line['type'] = 'customer' if line_elements[3] == customer_name else 'agent'
        parsed_line['sentence'] = line_elements[4]
        return parsed_line

    @staticmethod
    def get_line_elements(line):
        """Separates the elements of a single line such as date and mention in an array"""
        line_regex = r"((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w\s]+) : )(.+\n*))|((([0-9][0-9]:[0-9][0-9]:[0-9][0-9]) ([\w]+) )(.+\n*))"
        line_elements = re.search(line_regex, line)
        clean_line_elements = [x for x in line_elements.groups() if x !=
                               '' and x != None] # Removes empty elements
        return clean_line_elements

    @staticmethod
    def split_dates(chat):
        """Splits the whole chat by using dates"""
        date_splitter_regex = r'([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w\s]+ :)|([0-9][0-9]:[0-9][0-9]:[0-9][0-9] [\w]+ )'
        split_chat_with_separators = re.split(date_splitter_regex, chat)
        clean_split_chat_with_separators = [
            x for x in split_chat_with_separators if x != '' and x != None] # Removes empty elements
        split_chat = [clean_split_chat_with_separators[i] + clean_split_chat_with_separators[i+1]
                      for i in range(0, len(clean_split_chat_with_separators)-1, 2)] # Couples separators and messages
        return split_chat

    @staticmethod
    def get_customer_name(customer_line):
        """Extracts customer name from a single line sent by the customer"""
        return ChatParser.get_line_elements(customer_line)[3]
