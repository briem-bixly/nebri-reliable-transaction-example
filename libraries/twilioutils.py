from twiliomodels import Message, MessageFetch
from twilio.rest import TwilioRestClient
import requests
import logging

logging.basicConfig(filename='twilio.log', level=logging.DEBUG)


def get_messages(sid, token):
    try:
        fetched = MessageFetch.filter()
        client = TwilioRestClient(sid, token)
        if fetched.length == 0:
            messages = client.messages.list()
        else:
            messages = client.messages.list(after=fetched.date_ran)
        message_count = 0
        for m in messages:
            message_count += 1
            url = '%s.json' % m.uri
            logging.debug(url)
            data = requests.get(url, auth=(sid, token)).content
            try:
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
            MessageFetch(
                date_ran=datetime.now(),
                num_messages_fetched=message_count
            )
        else:
            fetched.date_ran = datetime.now()
            fetched.num_messages_fetched = message_count
        fetched.save()
        return 'Success'
    except Exception, e:
        return 'Error: %s' % str(e)


def generate_outgoing_message(to, from_, body):
    message = Message()
    message.sms_to = to
    message.sms_from = from_
    message.sms_body = body
    message.save()


def send_message(sid, token, message_pid):
    message = Message.get(pid=message_pid)
    client = TwilioRestClient(sid, token)
    new_message = client.messages.create(
        to=message.sms_to,
        from_=message.sms_from,
        body=message.sms_body
    )
    return new_message.sid
