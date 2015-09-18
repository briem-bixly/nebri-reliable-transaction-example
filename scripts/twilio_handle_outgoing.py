from twiliomodels import Message
from twilioutils import send_message


class twilio_handle_outgoing(NebriOS):
    listens_to = ['sms_to', 'sms_from', 'sms_body']

    def check(self):
        return self.sms_to != '' and \
               self.sms_from != '' and \
               self.sms_body != '' and \
               self.sms_direction != 'incoming' and \
               self.sent == False
    def action(self):
        try:
            # do stuff with the message
            message_id = send_message(shared.twilio_sid, shared.twilio_token, self.pid)
            self.twilio_id = message_id
            self.date_sent = datetime.now()
            self.sent = True
        except:
            # something happened and we got an error... do nothing with this message.
            pass
