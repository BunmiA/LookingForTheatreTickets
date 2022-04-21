from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from twilio.rest import Client
import config
import time
from datetime import datetime
import logging

URL = "https://ticketing.almeida.co.uk/events/5403"

# Giphs can only be sent to american and canadian numbers
HAPPY_GIPH = "https://giphy.com/embed/5GoVLqeAOo6PK"
SAD_GIPH = "https://giphy.com/embed/l1AsyjZ8XLd1V7pUk"

logging.basicConfig(filename='LookingForTheatreTickets.log', level=logging.DEBUG)


def get_ticket_dates():
    # Scrapes website for chnage
    logging.debug('Getting ticket details')
    opts = Options()
    opts.set_headless()
    assert opts.headless  # Operating in headless mode
    browser = Firefox(options=opts)
    browser.get(URL)

    # Getting Theatre Dates
    result = browser.find_elements_by_css_selector('span.tn-prod-list-item__perf-date')
    dates = [date.text for date in result if date.text != '']

    # Getting Play Times
    result = browser.find_elements_by_css_selector('span.tn-prod-list-item__perf-time')
    times = [time.text for time in result if time.text != '']

    # Getting Play Ticket Status
    result = browser.find_elements_by_css_selector('span.tn-prod-list-item__perf-property--action')
    status = [status.text for status in result if status.text != '']

    # Asserts that data is accurate and equal in length
    assert len(times) == len(dates) == len(status), 'Data lengths not matching'

    # looking for avaliable dates
    available_dates = []
    for i in range(len(status)):
        if status[i] not in ['Tickets not on sale', 'Sold out']:
            available_dates.append(i)

    return available_dates, zip(dates, times, status)


def should_send_text(available_dates):
    # This method helps avoid sending messages every hour if no dates
    logging.debug('Checking if we should send message')
    now = datetime.now()
    if (now.hour == config.NO_TICKET_TEXT_TIME and now.minute < 5) or len(available_dates) > 0:
        logging.debug('will be sending an text')
        return True
    return False


def create_text(available_dates, ticket_data):
    if len(available_dates) == 0:
        return 'No tickets available :(', SAD_GIPH
    return 'Great News!!!, There are tickets for "DADDY" A MELODRAMA on these dates {} . Book at {}'.format(str([ticket_data[a] for a in available_dates]),
                                                                                                            URL), HAPPY_GIPH


def send_text(message_body, gipy):
    # Uses Twilio to find
    account_sid = config.TWILIO_ACCOUNT_SID
    auth_token = config.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body =message_body,
            from_=config.TWILIO_NUMBER,
            # media_url=[giph_url],
            to=config.MY_NUMBER
        )
    except:
        logging.warn('not sure if text was sent')


if __name__ == "__main__":
    available_dates, ticket_data = get_ticket_dates()
    if should_send_text(available_dates):
        message_body, giph_url = create_text(available_dates, ticket_data)
        send_text(message_body, giph_url)
