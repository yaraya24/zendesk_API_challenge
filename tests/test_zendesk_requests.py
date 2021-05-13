import unittest
from unittest.mock import Mock, patch
from ZendeskRequests import TicketRequests, ZendeskRequest
import config


class test_ticket_requests(unittest.TestCase):
    def setUp(self):
        self.ticket_request = TicketRequests(
            "soontobeintern",
            {
                "Authorization": "Bearer e334541a32fc92914a5f30a168ebead13182b481d754170f953fc92cc5ee6ece"
            },
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
        self.assertEqual(len(summary_ticket_data[0]), len(config.SUMMARY_TICKET_ATTRIBUTES))
        self.assertIsInstance(summary_ticket_data[0], dict)
        self.assertIsNotNone(summary_ticket_data[0]['id'])
        self.assertIsNotNone(summary_ticket_data[0]['subject'])
        self.assertIsNotNone(summary_ticket_data[0]['requester_id'])
        self.assertIsNotNone(summary_ticket_data[0]['assignee_id'])

    def test_get_detailed_ticket_data(self):
        pass


    # @patch("ZendeskRequests.requests.get")
    # def test_get_tickets_mocked(self, mock_get):

    #     mock_get.status_code = 200

    #     response = TicketRequests(
    #         "soontobeintern",
    #         {
    #             "Authorization": "Bearer e334541a32fc92914a5f30a168ebead13182b481d754170f953fc92cc5ee6ece"
    #         },
    #         "tickets.json",
    #     )
    #     self.assertIsNotNone(response)
    #     # self.assertTrue(response.json(), True)
    #     self.assertTrue(response.status_code, 200)
