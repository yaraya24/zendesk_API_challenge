# Zendesk Coding Challenge

A command line application that consumes the Zendesk API to retrieve and display tickets associated with a particular account. The program utilises the request module to make GET requests to the tickets endpoint of the Zendesk API and display them formatted. 



### Requirements:

* Python3
* Pip
* Internet Connection to connect to the API



### Installation:

1. Clone the repository into your local machine

```
git clone https://github.com/yaraya24/zendesk_API_challenge.git
```

2. Go into the project directory and create a virtual environment

```
python3 -m venv venv
```

3. Activate the virtual environment and then install the dependencies.

```
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the application

```
python main.py
```

5. Create a .env file with the subdomain name and the OAuth token. Information on obtaining an OAuth token can be found on https://support.zendesk.com/hc/en-us/articles/203663836-Using-OAuth-authentication-with-your-application. An example .env file is provided in the repo.

```
SUBDOMAIN='your subdomain'
TOKEN='your OAuth token '
```



6. Tests can be run with the command:

```
python -m unnitest discover
```



### How to use:

Once the application has been successfully installed and executed, you can navigate through the CLI using the numbers next to the options that are presented.

```
Options:
1. View Tickets
2. Exit
```

Anything provided that isn't a number associated with an option will be disregarded.

You are able to search for detailed information on a ticket by providing the id. As a separate request is being made with a query containing the ticket id, you are not limited to searching tickets that are currently present in the summary page.



#### Notes to assessors:

* I understand that the coding challenge has a gotcha that requests the use of basic authentication. However, due to using my personal email and staff suggestions that it only a starting point and to read further, I have decided to use OAuth and attempt to adhere to security best practices. 