from twiliomodels import Message


class twilio_handle_incoming(NebriOS):
    listens_to = ['raw_data']

    def check(self):
        return self.raw_data != '' and self.handled == False

    def action(self):
        # Do stuff with incoming message
        self.date_handled = datetime.now()
        self.handled = True
