from twilioutils import send_message


class twilio_retry_send(NebriOS):
    listens_to = ['twilio_retry_send']

    def check(self):
        return shared.twilio_sid != None and /
               shared.twilio_token != None and /
               self.twilio_retry_send == True

    def action(self):
        # for debouncing purposes
        self.twilio_retry_send = 'Ran'
        pending_messages = Message.filter(sent=False, sms_direction='')
        for message in pending_messages:
            try:
                # do stuff with message
                message_id = send_message(shared.twilio_sid, shared.twilio_token, message.pid)
                message.twilio_id = message_id
                message.date_sent = datetime.now()
                message.sent = True
                message.save()
            except:
                # something happened and we got an error... do nothing with this message.
                pass
