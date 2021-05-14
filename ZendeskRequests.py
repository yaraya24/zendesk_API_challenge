import requests
import config
import sys


class ZendeskRequest:

    """Absract parent class that allows for connection to Zendesk's API"""

    def __init__(self, subdomain, authorization):
        """initialisation of class attributes that are required to connect to Zendesk API"""
        self.subdomain = subdomain
        self.authorization = authorization
        self.url = f"https://{subdomain}.zendesk.com/api/v2/"

    def get(self, endpoint, params={}):
        """Class method that returns tuple with string response message and the response if available"""

        try:
            response = requests.get(
                self.url + endpoint,
                headers=self.authorization,
                params=params,
                timeout=2,
            )
            response.raise_for_status()  # method that raises exceptions if status code is not 200
            return "Success", response
        except requests.exceptions.HTTPError as e:
            return "Error", e.response.json()["error"]
        except requests.exceptions.Timeout:
            return "Error", "Connection has timed out"
        except requests.exceptions.ConnectionError:
            return "Error", "There has been a connection error"
        except Exception as e:
            return "Error", e


class TicketRequests(ZendeskRequest):

    """Class that inherits from Zendesk request and is an implementation of the parent class for tickets"""

    def __init__(self, subdomain, authorization, endpoint):
        """Initialisation of the attributes that are specific for making ticket requests"""
        super().__init__(subdomain, authorization)
        self.endpoint = endpoint
        self.params = config.PAGINATION_SIZE.copy()
        self.response_data = None
        self.response_data_json = None
        self.ticket_data = None
        self.pagination_data = None
        self.get()

    def get(self):
        """Method that uses the get method from ZendeskRequest to make a specific request to the tickets endpoint.
        Stores the response data in attributes that are used for methods"""

        self.response_data = super().get(self.endpoint, self.params)
        if self.response_data[0] == "Success":
            self.response_data_json = self.response_data[1].json()
            self.ticket_data = self.response_data_json["tickets"]
            self.pagination_data = self.response_data_json["meta"]
            self.params = config.PAGINATION_SIZE.copy()
        else:
            print(self.response_data[1])
            return False

    def display_summary_ticket_data(self):
        """Prints a summary of the ticket data retrieved from the API"""
        ticket_headers = {}
        for attribute in config.SUMMARY_TICKET_ATTRIBUTES:
            ticket_headers[attribute] = attribute.upper()

        summary_data_list = self.get_summary_ticket_data()
        if summary_data_list:
            print("\n")
            summary_ticket_data_with_headers = [ticket_headers] + summary_data_list
            for count, data in enumerate(summary_ticket_data_with_headers):
                print(
                    f'{data["id"]:<10} {data["subject"]:<60}{data["requester_id"]:<20}{data["assignee_id"]:>20}'
                )
                if count == 0:
                    print("=" * 112)
            return True
        else:
            return False

    def get_summary_ticket_data(self):
        """Method that crops the data retrieved from the API to only have summary attributes"""
        summary_ticket_data = []
        if self.ticket_data:
            for ticket in self.ticket_data:
                summary_ticket_data.append(
                    {
                        attribute: ticket[attribute]
                        for attribute in config.SUMMARY_TICKET_ATTRIBUTES
                    }
                )
            return summary_ticket_data
        else:
            return False

    def get_detailed_ticket_data(self, ticket_id):
        """Method that makes a request to Zendesk API with a ticket ID to get detailed information on that one ticket"""

        if ticket_id.isdigit():
            ticket_search_result = super().get("search.json", {"query": ticket_id})
            if ticket_search_result[0] == "Success":
                detailed_ticket_result = ticket_search_result[1].json()["results"]
                if detailed_ticket_result:
                    self.display_detailed_ticket_data(
                        self.crop_ticket_data_to_detailed_attributes(
                            detailed_ticket_result[0]
                        )
                    )
                else:
                    print("\033[31m" + "Unable to find that ticket" + "\033[0m")
            else:
                print(ticket_search_result[0])
        else:
            print("\033[31m" + "Please enter a valid id" + "\033[0m")

    def crop_ticket_data_to_detailed_attributes(self, detailed_ticket):
        """Method that crops the detailed ticket data to only have attributes from the detailed ticket attributes list"""
        return {
            attribute: detailed_ticket[attribute]
            for attribute in config.DETAILED_TICKET_ATTRIBUTES
        }

    def display_detailed_ticket_data(self, cropped_detail_ticket):
        """Prints the detailed ticket data to screen"""
        print("\n *** DETAILED TICKET INFORMATION ***")
        for attribute in config.DETAILED_TICKET_ATTRIBUTES:
            print(f"{attribute.upper()} : {cropped_detail_ticket[attribute]} ")

        input('\n Press "ENTER" to continue...')

    def check_if_next_page_available(self):
        """Method that returns boolean depending on whether there is further pagination available"""
        return self.pagination_data["has_more"]

    def get_next_page(self):
        """Makes another API request to get the next page of data and consequently updates instance attributes"""
        self.params["page[after]"] = self.pagination_data["after_cursor"]
        self.get()

    def check_if_prev_page_available(self):
        """Method that returns boolean if previous page is available, required to make api call due to using cursor pagination"""
        check_previous = super().get(
            self.endpoint, {"page[before]": self.pagination_data["before_cursor"]}
        )[1]
        if check_previous.json()["tickets"]:
            return True
        else:
            return False

    def get_prev_page(self):
        """Makes API call to get previous page of data and consequently updates instance attributes"""
        self.params["page[before]"] = self.pagination_data["before_cursor"]
        self.get()

    def get_all_data(self):
        return self.response_data
