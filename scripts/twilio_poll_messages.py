from twilioutils import get_messages


class twilio_poll_messages(NebriOS):
    schedule = "0 0 * * *"

    def check(self):
        return self.sid != None and self.token != None

    def action(self):
        get_messages(self.sid, self.token)
