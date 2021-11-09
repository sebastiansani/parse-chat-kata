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

def chat_parser(chat):
    if chat is None or chat == '':
        return []
    parsed_chat = []
    sentence = {}
    split_sentence = chat.split(' ')
    sentence['date'] = split_sentence[0]
    sentence['mention'] = split_sentence[0] + ' ' + split_sentence[1] + ' : '
    sentence['sentence'] = ' '.join(split_sentence[3:])
    sentence['type'] = split_sentence[1].lower()
    parsed_chat.append(sentence)
    return parsed_chat