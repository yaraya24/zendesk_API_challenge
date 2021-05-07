from ZendeskRequests import TicketRequests
from menu import Menu
import sys

def main():
    menu_options = [
        'View Tickets',
        'Help',
        'Exit'
    ]
    print("ZENDESK TICKETING SYSTEM")
    print("=" * 112)  
    first_page_menu = Menu(menu_options)
    selection = first_page_menu.display_options()

    if selection == menu_options[0]:
        ticket_summary_page()
    elif selection == menu_options[1]:
        help_page()
    else:
        sys.exit()
    


def ticket_summary_page():
    # credentials = api_credentials()
    zendesk_tickets = TicketRequests('soontobeintern', {'Authorization': 'Bearer e334541a32fc92914a5f30a168ebead13182b481d754170f953fc92cc5ee6ece'}, 'tickets.json')
    
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
                    print("There are no more records to show")
            elif selection == ticket_summary_options[1]:
                if zendesk_tickets.check_if_prev_page_available():
                    zendesk_tickets.get_prev_page()
                    ticket_summary = zendesk_tickets.display_summary_ticket_data()
                    continue
                else:
                    print("There are no previous records to show")
            elif selection == ticket_summary_options[2]:
                 ticket_id = input("Please enter the ticket ID")
                 zendesk_tickets.get_detailed_ticket_data(ticket_id)
            elif selection == ticket_summary_options[4]:
                sys.exit()


                

        else:
            main()
            break
        
    

def help_page():
    print("HELP PAGE")
    menu_options = ['Back', 'Quit']
    help_page_menu = Menu(menu_options)
    selection = help_page_menu.display_options()
    if selection == menu_options[0]:
        main()
    elif selection == menu_options[1]:
        sys.exit()

def api_credentials():
    print("### Login to Zendesk API ###")
    credentials = {}
    credentials['subdomain'] = input("Please enter your subdomain for Zendesk: \n")
    credentials['email'] = input("Please enter your email address: \n")
    credentials['password'] = input("Please enter your password: \n")
    return credentials



main()

