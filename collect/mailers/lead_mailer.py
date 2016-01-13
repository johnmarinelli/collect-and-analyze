from django.core.mail import send_mail

class LeadMailer:
    @staticmethod
    def send_mail(subject, body, recipient):
        sender = 'john@johnmarinelli.me'
        success = send_mail(subj, body, sender, [recipient, sender], fail_silently = False)
        return success

