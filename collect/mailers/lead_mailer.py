from django.core.mail import send_mail

class LeadMailer:
    @staticmethod
    def send_mail(subject, body, recipient):
        success = send_mail(subj, body, 'john@johnmarinelli.me', [recipient], fail_silently = False)
        return success

