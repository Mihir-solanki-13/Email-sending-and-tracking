from django.views.decorators.csrf import csrf_exempt
from email_app.models import Email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

@csrf_exempt
def email_opened(request, email_id):
    print('opened')
    print(email_id)
    email = get_object_or_404(Email, id=email_id)
    email.is_opened = True  # Update the 'is_opened' field
    email.save()  # Save the model
    return HttpResponse("Email opened")


def send(subject, body, recipient):
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient]

    email = EmailMultiAlternatives(
        subject,
        body,
        from_email,
        to,
    )

    try:
        email.send()
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
        
    
    # Build the URL using the tracking token
        # opened_email_url = request.build_absolute_uri(reverse('email_opened', kwargs={'tracking_token': tracking_token}))
        opened_email_url = request.build_absolute_uri(reverse('email_opened', kwargs={'email_id': email.id}))
        image_tag = f"<img src='{opened_email_url}' alt='Email Tracking' />"

        # Modify the message body to include the image tag
        body_with_image = f"{body} {image_tag}"
        email.body = body_with_image
        email.save()
        
        mail_sent = send(subject, body_with_image, recipient)

        if mail_sent:
            messages.success(request, "Mail sent successfully!")
            # Redirect to the same page with success message
            return redirect('/')
        else:
            messages.error(request, "Something went wrong. Mail not sent.")
            # Redirect to the same page with error message
            return redirect('/')

    return render(request, 'home.html')
