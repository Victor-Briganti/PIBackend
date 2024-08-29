from django.core.mail import send_mail
from django.conf import settings


def send_adoption_email(email, message):
    send_mail(
        "Adoção",
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )