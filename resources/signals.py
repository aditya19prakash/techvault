from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import google.generativeai as genai
from .models import Resource
from aiservice.ai_summarizer import email_message_creation
from .serializers import ResourceSignalsSerializerID
import threading

LOGO_URL = "https://raw.githubusercontent.com/aditya19prakash/techvault/main/unnamed.jpg"
def run_async(func, *args, **kwargs):
    """Run any function in a background thread."""
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()

    
def process_resource_email(instance):
    receivers = [
        "adyprakash19@gmail.com"
    ]
    serializer = ResourceSignalsSerializerID(instance)
    email_text = email_message_creation(serializer.data)
    for r in receivers:
        send_email_with_image_url(r, email_text)

def send_email_with_image_url(to_email, email_text):
    subject = "Project Summary - TechVault"
    from_email = settings.SENDER
    email_html_text = email_text.replace("\n", "<br>")
    html_body = f"""
    <div style="text-align:center;">
        <img src="{LOGO_URL}" alt="TechVault Logo"
             style="width:180px; margin-bottom:20px;" />
    </div>

    <div style="font-family:Arial; font-size:15px;">
        {email_html_text}
    </div>
    """

    email = EmailMultiAlternatives(subject, "", from_email, [to_email])
    email.attach_alternative(html_body, "text/html")
    email.send()



@receiver(post_save, sender=Resource)
def send_resource_added_email(sender, instance, created, **kwargs):
    if not created:
        return
    run_async(process_resource_email, instance)

