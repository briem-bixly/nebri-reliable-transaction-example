from twiliomodels import Message


class twilio_handle_incoming(NebriOS):
    listens_to = ['raw_data']

    def check(self):
        return self.raw_data != '' and self.handled == False

    def action(self):
        # Do stuff with incoming message
        if self.status == 'undelivered' or self.status == 'failed':
            # check raw_data for more info
            error_code = self.raw_data['error_code']
            error_msg = self.raw_data['error_message']
            # handle based on error
        self.date_handled = datetime.now()
        self.handled = True
