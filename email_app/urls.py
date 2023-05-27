from django.urls import path ,re_path
# from views import *
from .views import *

urlpatterns = [
    path('', send_email, name='send_email'),
    path('email/opened/<int:email_id>/', email_opened, name='email_opened'),
]