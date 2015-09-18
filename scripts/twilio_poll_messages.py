from twilioutils import get_messages


class twilio_poll_messages(NebriOS):
    listens_to = ['twilio_poll_messages']

    def check(self):
        return shared.twilio_sid != None and \
               shared.twilio_token != None and \
               self.twilio_poll_messages == True

    def action(self):
        # for debouncing purposes
        self.twilio_poll_messages = 'Ran'
        get_messages(shared.twilio_sid, shared.twilio_token)
