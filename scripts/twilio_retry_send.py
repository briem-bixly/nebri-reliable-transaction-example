from twilioutils import send_message


class twilio_retry_send(NebriOS):
    schedule = "0 0 * * *"

    def check(self):
        return self.sid != None and self.token != None

    def action(self):
        pending_messages = Message.filter(sent=False)
        for message in pending_messages:
            try:
                message_id = send_message(self.sid, self.token, message.pid)
                message.twilio_id = message_id
                message.date_sent = datetime.now()
                message.sent = True
                message.save()
            except:
                # something happened and we got an error... do nothing with this message.
                pass
