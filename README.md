# LookingForTheatreTickets

## Description 
Python tool that scarps a theatre site looking to see if tickets has become available and sends text when avilaible

## Setup
This documentation assumes this is ran using a MAC OS with home brew and python 3 installed

## Installation

First get requirements

`pip install -r requirements.txt`

geckodriver is need for selenium to run

`brew geckodriver`

create a config.py file in directory  add the following details. 
Reference https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python for how to use twilio

```
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_NUMBER = ''
MY_NUMBER = ''
NO_TICKET_TEXT_TIME = 22
```

## Running
To run for a different URL update URL constant in main.py.
Also update the get_ticket_dates method to scrape the right elements from a new url

### Scheduling 

Open Crontab
`crontab -e`

enter schedule details thane save and close vi
`0 1 * * * python LookingForTheatreTickets/main.py`

This will run the scrape at minute = 0 , hour = 1, day = * : every day, month=: * every month, weekday= * every weekday.
Reference https://crontab.guru/ 

list Crontab jobs
`crontab -l`
