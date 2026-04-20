class Notification:
    types = {
        'email': 'EmailNotification',
        'sms': 'SMSNotification',
        'push': 'PushNotification'
    }

class EmailNotification(Notification):
    def send(self):
        print("Mail gönderildi!!!")
    
class SMSNotification(Notification):
    def send(self):
        print("SMS gönderildi!!!")
    
class PushNotification(Notification):
    def send(self):
        print("Push bildirimi gönderildi!!!")


class NotificationFactory:
    @staticmethod
    def create_notification(notification_type):
        if notification_type == "email":
            return EmailNotification()
        elif notification_type == "sms":
            return SMSNotification()
        elif notification_type == "push":
            return PushNotification()
        else:
            raise ValueError("Geçersiz notification type")
        

notif = NotificationFactory.create_notification("email")
notif.send()
