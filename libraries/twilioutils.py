from twiliomodels import Message, MessageFetch
from twilio.rest import TwilioRestClient
import requests
import logging

logging.basicConfig(filename='twilio.log', level=logging.DEBUG)


def get_messages(sid, token):
    try:
        # in order to keep from retrieving the same messages over and over, we keep track of the last time
        # we queried twilio
        fetched = MessageFetch.filter()
        client = TwilioRestClient(sid, token)
        if fetched.length == 0:
            messages = client.messages.list()
        else:
            # 'after' was found by digging through the api documentation in python-twilio. this has not been tested.
            # https://twilio-python.readthedocs.org/en/latest/api/rest/resources.html#sms-messages
            # this can be changed to date_sent with an inequality that will retrieve all messages sent/received after
            # or before the date depending on inequality. 
            messages = client.messages.list(after=fetched.date_ran)
        message_count = 0
        for m in messages:
            message_count += 1
            # twilio doesn't send a json representation back, so we need to make a second query to get storable
            # data
            url = '%s.json' % m.uri
            logging.debug(url)
            data = requests.get(url, auth=(sid, token)).content
            try:
                # let's check to see if this message already exists
                message = Message.get(twilio_id=m.sid)
                # update message instance
                message.sms_to = m.to
                message.sms_from = m.from_
                message.sms_body = m.body
                message.sms_status = m.status
                message.sms_direction = m.direction
                message.raw_data = data
            except:
                # create new instance
                message = Message(
                    twilio_id=m.sid,
                    sms_to=m.to,
                    sms_from=m.from_,
                    sms_body=m.body,
                    sms_status=m.status,
                    sms_direction=m.direction,
                    raw_data=data,
                )
            message.save()
        if fetched.length == 0:
            # this is the first time we've fetched messages... create an entry
            MessageFetch(
                date_ran=datetime.now(),
                num_messages_fetched=message_count
            )
        else:
            # update the existing entry
            fetched.date_ran = datetime.now()
            fetched.num_messages_fetched = message_count
        fetched.save()
        return 'Success'
    except Exception, e:
        return 'Error: %s' % str(e)


def generate_outgoing_message(to, from_, body):
    # to and from_ should be 10 digit phone number strings with a '+' preceding the number
    message = Message()
    message.sms_to = to
    message.sms_from = from_
    message.sms_body = body
    message.save()
    # saving should trigger the handle_outgoing script to actually send the message


def send_message(sid, token, message_pid):
    message = Message.get(pid=message_pid)
    client = TwilioRestClient(sid, token)
    new_message = client.messages.create(
        to=message.sms_to,
        from_=message.sms_from,
        body=message.sms_body
    )
    # once this is created on our twilio instance, return twilio's sid
    # this will help with debouncing and will give our get_messages function an object to update instead of
    # creating duplicates
    return new_message.sid
