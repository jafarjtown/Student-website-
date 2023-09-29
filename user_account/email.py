from django.core.mail import send_mail, mail_admins


def send_email_message(subject, message, receivers):
    
    return send_mail(
        subject,
        message,
        'from@example.com',
        receivers,
        fail_silently=False,
    )
    
def send_email_message_admin(subject, message):
    return mail_admin(subject, message)