from twilio.rest import Client

class Notifier:
        def __init__(self, account, token, from_num, to_num):
                self.account = account
                self.token = token
                self.from_num = from_num
                self.to_num = to_num

        def send_sms_alert(self, msg):
                client = Client(self.account, self.token)
                message = client.messages \
                          .create(body=msg,
                                  from_=self.from_num,
                                  to=self.to_num
                                 )

