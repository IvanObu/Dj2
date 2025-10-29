from django.urls import path
from . import views, webhooks

app_name='payment'

urlpatterns = [
    path("process/", views.payment_process, name='process'),
    path("complited/", views.payment_complited, name='complited'),
    path("canceled/", views.payment_canceled, name='canceled'),
    # path("webhook/", views.payment_webhook, name='webhook'),
]
