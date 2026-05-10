from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_plain_email(to, subject, body, from_email=None):
    if isinstance(to, str):
        to = [to]
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        recipient_list=to,
    )


def send_template_email(to, subject, template_name, context, from_email=None):
    if isinstance(to, str):
        to = [to]
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
