import requests
import config
import sys


class ZendeskRequest:

    """ Absract parent class that allows for connection to Zendesk's API"""

    def __init__(self, subdomain, authorization):
        self.subdomain = subdomain
        self.authorization = authorization
        self.url = f"https://{subdomain}.zendesk.com/api/v2/"


    def get(self, endpoint, params={}):
        try:
            response = requests.get(self.url + endpoint, headers=self.authorization, params=params, timeout=2)
            response.raise_for_status()
            return 'Success', response
        except requests.exceptions.HTTPError as e:
            return 'Error', e.response.json()['error']
        except requests.exceptions.Timeout:
            return 'Error', 'Connection has timed out'
        except requests.exceptions.ConnectionError:
            return 'Error', 'There has been a connection error'
        except Exception as e:
            return 'Error', e
        



class TicketRequests(ZendeskRequest):

    def __init__(self, subdomain, authorization, endpoint):
        super().__init__(subdomain, authorization)
        self.endpoint = endpoint
        self.params = config.PAGINATION_SIZE.copy()
        self.response_data = None
        self.response_data_json = None
        self.ticket_data = None
        self.pagination_data = None
        self.get()

    def get(self):
        
        self.response_data = super().get(self.endpoint, self.params)
        if self.response_data[0] == 'Success':
            self.response_data_json = self.response_data[1].json()
            self.ticket_data = self.response_data_json['tickets']
            self.pagination_data = self.response_data_json['meta']
            self.params =  config.PAGINATION_SIZE.copy()
        else:
            print(self.response_data[1])
            return False
        
    def display_summary_ticket_data(self):
        ticket_headers = {}
        for attribute in config.SUMMARY_TICKET_ATTRIBUTES:
            ticket_headers[attribute] = attribute.upper()
        
        
        summary_data_list = self.get_summary_ticket_data()
        if summary_data_list:
            print('\n')
            summary_ticket_data_with_headers = [ticket_headers] + summary_data_list
            for count, data in enumerate(summary_ticket_data_with_headers):
                print(f'{data["id"]:<10} {data["subject"]:<60}{data["requester_id"]:<20}{data["assignee_id"]:>20}')
                if count == 0:
                    print("=" * 112)
            return True
        else:
            return False
       

    def get_summary_ticket_data(self):
        summary_ticket_data = []
        if self.ticket_data:
            for ticket in self.ticket_data:
                summary_ticket_data.append(
                    {attribute : ticket[attribute] for attribute in config.SUMMARY_TICKET_ATTRIBUTES}
                )
            return summary_ticket_data
        else:
            return False

    
    def get_detailed_ticket_data(self, ticket_id):
        ticket_search_result = super().get('search.json', {'query': ticket_id})
        if ticket_search_result[0] == 'Success':
            detailed_ticket_result = ticket_search_result[1].json()['results']
            if detailed_ticket_result:
                self.display_detailed_ticket_data(self.crop_display_ticket_data_to_detailed_attributes(detailed_ticket_result[0]))
            else:
                print('Unable to find that ticket')
        else:
            print(ticket_search_result[0])

    def crop_display_ticket_data_to_detailed_attributes(self, detailed_ticket):
        return {attribute : detailed_ticket[attribute] for attribute in config.DETAILED_TICKET_ATTRIBUTES}

    def display_detailed_ticket_data(self, cropped_detail_ticket):
        
        print('\n *** DETAILED TICKET INFORMATION ***')
        for attribute in config.DETAILED_TICKET_ATTRIBUTES:
            print(f'{attribute.upper()} : {cropped_detail_ticket[attribute]} ')
        
        input('\n Press "ENTER" to continue...')
        
        
       


    def check_if_next_page_available(self):
        return self.pagination_data['has_more']

    def get_next_page(self): # decorator or something that will require the prev function to be true before it can be called
        self.params['page[after]'] = self.pagination_data['after_cursor']
        self.get() 
        

    def check_if_prev_page_available(self):
        check_previous = super().get(self.endpoint, {'page[before]': self.pagination_data['before_cursor']})[1]
        if check_previous.json()['tickets']:
            return True
        else:
            return False

    def get_prev_page(self):
        self.params['page[before]'] = self.pagination_data['before_cursor']
        self.get()
        

    def get_all_data(self):
        return self.response_data
        
    


