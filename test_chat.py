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

    def test_chat_parser_multiple_sentences(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                "14:26:15 Agent : Aliquam non cursus erat, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Agent : ",
            "sentence": "Aliquam non cursus erat, ut blandit lectus.",
            "type": "agent"
        }])

    def test_chat_parser_two_customer_mentions_as_start(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = (
            "14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "14:27:00 Customer : Pellentesque cursus maximus felis, pharetra porta purus aliquet viverra.\n"
            "14:27:47 Agent : Vestibulum tempor diam eu leo molestie eleifend.\n"
            "14:28:28 Customer : Contrary to popular belief, Lorem Ipsum is not simply random text."
        )
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
            "type": "customer"
        }, {
            "date": "14:27:00",
            "mention": "14:27:00 Customer : ",
            "sentence": "Pellentesque cursus maximus felis, pharetra porta purus aliquet viverra.\n",
            "type": "customer"
        }, {
            "date": "14:27:47",
            "mention": "14:27:47 Agent : ",
            "sentence": "Vestibulum tempor diam eu leo molestie eleifend.\n",
            "type": "agent"
        }, {
            "date": "14:28:28",
            "mention": "14:28:28 Customer : ",
            "sentence": "Contrary to popular belief, Lorem Ipsum is not simply random text.",
            "type": "customer"
        }])

    def test_chat_parser_date_splitting(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                "14:26:15 Agent : Aliquam non cursus erat, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Agent : ",
            "sentence": "Aliquam non cursus erat, ut blandit lectus.",
            "type": "agent"
        }])

    def test_chat_parser_ignore_extra_dates(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Customer : Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                "14:26:15 Agent : I received it at 12:24:48, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Agent : ",
            "sentence": "I received it at 12:24:48, ut blandit lectus.",
            "type": "agent"
        }])

    def test_chat_parser_full_name_date_separation(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Luca Galasso : Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                "14:26:15 Emanuele Querzola : I received the package, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Luca Galasso : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Emanuele Querzola : ",
            "sentence": "I received the package, ut blandit lectus.",
            "type": "agent"
        }])

    def test_chat_parser_full_name_newline_separation(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Luca Galasso : Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                "14:26:15 Emanuele Querzola : I received the package, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Luca Galasso : ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Emanuele Querzola : ",
            "sentence": "I received the package, ut blandit lectus.",
            "type": "agent"
        }])

    def test_missing_colon_after_names_date_separation(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Customer Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                "14:26:15 Agent I received it at 12:24:48, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Agent ",
            "sentence": "I received it at 12:24:48, ut blandit lectus.",
            "type": "agent"
        }])

    def test_missing_colon_after_names_newline_separation(self):
        # Note: chat variable contains a single string, this format is used for readability.
        chat = ("14:24:32 Customer Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                "14:26:15 Agent I received it at 12:24:48, ut blandit lectus.")
        parsed_chat = chat_parser(chat)
        self.assertEqual(parsed_chat, [{
            "date": "14:24:32",
            "mention": "14:24:32 Customer ",
            "sentence": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
            "type": "customer"
        }, {
            "date": "14:26:15",
            "mention": "14:26:15 Agent ",
            "sentence": "I received it at 12:24:48, ut blandit lectus.",
            "type": "agent"
        }])


if __name__ == "__main__":
    unittest.main()
