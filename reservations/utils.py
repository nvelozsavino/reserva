from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import settings

def send_html_email(subject, from_email, to, template, variables):
    variables['SITE_URL']=settings.SITE_URL
    variables['STATIC_URL']=settings.SITE_URL + settings.STATIC_URL
    html_content = render_to_string(template, variables) # ...
    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.preserve_recipients=False
    msg.send()