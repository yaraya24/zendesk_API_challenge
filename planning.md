# Plan for Zendesk API Challenge:

## Requirements/Functionality:

 * Connect to the Zendesk API (requests module)
 * Request all tickets for an account (using email as id?)
 * Display all tickets in a list 
 * Display individual tickets 
 * Page through tickets when more than 25 are retrieved (pagination offerred in API docs)


## Non-Functional Requirements:

 * Readme with installation and usage
 * Amount of data displayed in the list format for all tickets and amount of data on individual tickets is up to me
 * Ticket viewer should handle API not being available
 * write happy path tests?
 * Submission can be done by emailing repo address


# Strategy and Design:

* Using request module, can make API requests, parse the JSON data that is returned




## Things to figure out:

 * How am I going to manage pagination? I can do it on the client side or the server side
 * Should I make it asynchronous??\
 * How do I design the code (OOP) - what classes do I need?


 # Security Concerns:

 * Right now we using basic authentication....
 * Consider OAuth or Token Authentication?


 ## NAVIGATION:

 * Main Menu:
        - Connect to Zendesk API
        - ReadMe
        - Quit


    * ZendDesk API
         - Requests your username, domain and password
                     - if successful, provide list of all tickets
                     - can select an individual ticket
                            - if ticket selected shows the ticket, can back
                    - can move forward and back