from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference


class Usage(NebriOSModel):
    usage_type = NebriOSField(required=True)
    date_received = NebriOSField(required=True, default=datetime.now)
    twilio_id = NebriOSField(required=True)
    raw_data = NebriOSField(required=True)


class Error(NebriOSModel):
    date_received = NebriOSField(required=True, default=datetime.now)
    twilio_id = NebriOSField(required=True)
    raw_data = NebriOSField(required=True)


class Message(NebriOSModel):
    date_created = NebriOSField(required=True, default=datetime.now)
    twilio_id = NebriOSField()
    sms_to = NebriOSField(required=True)
    sms_from = NebriOSField(required=True)
    sms_body = NebriOSField(required=True)
    sms_status = NebriOSField()
    sms_direction = NebriOSField()
    raw_data = NebriOSField()
    sent = NebriOSField(required=True, default=False)
    date_sent = NebriOSField()
    handled = NebriOSField(required=True, default=False)
    date_handled = NebriOSField()


class MessageFetch(NebriOSModel):
    date_ran = NebriOSField(required=True, default=datetime.now)
    num_messages_fetched = NebriOSField(required=True)
