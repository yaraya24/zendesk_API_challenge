from ZendeskRequests import TicketRequests
from menu import Menu
import config
import sys
from dotenv import load_dotenv
from os import environ

def main():
    load_dotenv()

    menu_options = [
        'View Tickets',
        'Exit'
    ]
    print("ZENDESK TICKETING SYSTEM")
    print("=" * 112)  
    first_page_menu = Menu(menu_options)
    selection = first_page_menu.display_options()

    if selection == menu_options[0]:
        ticket_summary_page()
    else:
        sys.exit()
    


def ticket_summary_page():
    
    zendesk_tickets = TicketRequests(environ.get('SUBDOMAIN'), {'Authorization': environ.get('TOKEN')}, 'tickets.json')
    
    while True:
        ticket_summary = zendesk_tickets.display_summary_ticket_data()
        if ticket_summary:
            ticket_summary_options = ['Next Page','Previous Page', 'Detail View', 'Back', 'Quit']
            summary_ticket_page_menu = Menu(ticket_summary_options)
            selection = summary_ticket_page_menu.display_options()

            if selection == ticket_summary_options[0]:
                if zendesk_tickets.check_if_next_page_available():
                    zendesk_tickets.get_next_page()
                    ticket_summary = zendesk_tickets.display_summary_ticket_data()
                    continue
                else:
                    print('\033[31m' + "There are no more records to show" + '\033[0m')
            elif selection == ticket_summary_options[1]:
                if zendesk_tickets.check_if_prev_page_available():
                    zendesk_tickets.get_prev_page()
                    ticket_summary = zendesk_tickets.display_summary_ticket_data()
                    continue
                else:
                    print('\033[31m' + "There are no previous records to show" + '\033[0m')
            elif selection == ticket_summary_options[2]:
                 ticket_id = input("Please enter the ticket ID: ")
                 zendesk_tickets.get_detailed_ticket_data(ticket_id)
            elif selection == ticket_summary_options[3]:
                 main()
            elif selection == ticket_summary_options[4]:
                sys.exit()


                

        else:
            main()
            break

main()

