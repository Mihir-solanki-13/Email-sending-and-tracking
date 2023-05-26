from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email_app.models import Email
from django.shortcuts import render ,redirect
from django.http import request
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string,get_template
from django.utils.html import strip_tags
import uuid
# from .models import TrackingData  # Import your TrackingData model from your app's models.py

# def save_tracking_identifier(tracking_identifier, recipient):
#     # Save the tracking identifier and recipient to your database
#     # tracking_data = TrackingData(tracking_identifier=tracking_identifier, recipient=recipient)
#     tracking_data.save()

    
def generate_tracking_identifier():
    # Generate a random UUID
    tracking_id= str(uuid.uuid4())

    # You can add additional processing or formatting if needed
    # For example, you can remove hyphens from the UUID
    tracking_id = tracking_id.replace('-', '')

    return tracking_id

def track_email(tracking_identifier, recipient):
    email = Email.objects.get(recipient=recipient)
    email.tracking_identifier = tracking_identifier
    email.save()


def send_verification_email(base_url, subject, body, recipient):
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient]

    email = EmailMultiAlternatives(
        subject,
        body,
        from_email,
        to,
    )

    tracking_identifier = str(uuid.uuid4())  # Generate a unique tracking identifier
    email_body_with_tracking = body + f"\n<img src='{base_url}/track/{tracking_identifier}/'>"

    try:
        email.send()
        # Save the tracking identifier and recipient to your database
        # save_tracking_identifier(tracking_identifier, recipient)
        return True
    except Exception as error:
        print("Exception while sending email to {}".format(to))
        print(error)
        return False

    


def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        recipient = request.POST.get('recipient')
        email = Email.objects.create(subject=subject, body=body, recipient=recipient)
        base_url = request.build_absolute_uri('/')
        mail_sent = send_verification_email(base_url,subject, body, recipient)

        if mail_sent:
            messages.success(request, "Mail sent successfully!")
            # Redirect to the same page with success message
            return redirect('/')
        else:
            messages.error(request, "Something went wrong. Mail not sent.")
            # Redirect to the same page with error message
            return redirect('/')

    return render(request, 'home.html')
