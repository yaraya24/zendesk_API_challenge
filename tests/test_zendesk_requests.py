import unittest
from unittest.mock import patch
from os import environ
from dotenv import load_dotenv
from ZendeskRequests import TicketRequests
import config


class test_ticket_requests(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.ticket_request = TicketRequests(
            environ.get("SUBDOMAIN"),
            {"Authorization": environ.get("TOKEN")},
            "tickets.json",
        )

    def test_get_ticket_without_mock(self):
        self.assertEqual(self.ticket_request.response_data[0], "Success")
        self.assertEqual(self.ticket_request.response_data[1].status_code, 200)
        self.assertEqual(len(self.ticket_request.ticket_data), 25)
        self.assertEqual(self.ticket_request.params, config.PAGINATION_SIZE)
        self.assertIsNotNone(self.ticket_request.pagination_data)

    def test_summary_ticket_data(self):
        summary_ticket_data = self.ticket_request.get_summary_ticket_data()
        self.assertEqual(len(summary_ticket_data), 25)
        self.assertEqual(
            len(summary_ticket_data[0]), len(config.SUMMARY_TICKET_ATTRIBUTES)
        )
        self.assertIsInstance(summary_ticket_data[0], dict)
        self.assertIsNotNone(summary_ticket_data[0]["id"])
        self.assertIsNotNone(summary_ticket_data[0]["subject"])
        self.assertIsNotNone(summary_ticket_data[0]["requester_id"])
        self.assertIsNotNone(summary_ticket_data[0]["assignee_id"])

    @patch("ZendeskRequests.print")
    def test_get_detailed_ticket_data(self, mock_print):
        self.ticket_request.get_detailed_ticket_data("a")
        mock_print.assert_called()
        mock_print.assert_called_with(
            "\033[31m" + "Please enter a valid id" + "\033[0m"
        )
        self.ticket_request.get_detailed_ticket_data("9999999")
        mock_print.assert_called_with(
            "\033[31m" + "Unable to find that ticket" + "\033[0m"
        )

    def test_pagination(self):
        self.assertIsNotNone(self.ticket_request.pagination_data)
        self.assertTrue(self.ticket_request.check_if_next_page_available())
        first_page = self.ticket_request.ticket_data
        self.ticket_request.get_next_page()
        self.assertNotEqual(first_page, self.ticket_request.ticket_data)
        self.assertTrue(len(self.ticket_request.ticket_data), 25)
        self.assertTrue(self.ticket_request.check_if_prev_page_available())
        self.ticket_request.get_prev_page()
        self.assertFalse(self.ticket_request.check_if_prev_page_available())
