"""
Chat parser tests.
"""

import unittest

from chat import chat_parser


class TestChatParser(unittest.TestCase):

    def setUp(self):
        pass

    def test_chat_parser_returns_a_list(self):
        self.assertIsInstance(chat_parser(""), list)

    def test_chat_parser_empty_string(self):
        self.assertEqual(chat_parser(""), [])

    def test_chat_parser_single_sentence(self):
        chat = "14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "type": "customer"
        }])

if __name__ == "__main__":
    unittest.main()
