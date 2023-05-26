from django.urls import path ,re_path
# from views import *
from .views import *

urlpatterns = [
    path('', send_email, name='send_email'),
    # path('track-email-open/', track_email_open, name='track_email_open'),
    # re_path(r'^image_load/$', image_load, name='image_load'),

    # path('track/<int:email_id>/', track_open, name='track_open'),
]