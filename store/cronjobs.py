from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from .models import Order


def remind_payments():
    tomorrow = datetime.now() + timedelta(days=1)
    queryset = Order.objects.filter(payment_date__date=tomorrow.date())
    for order in queryset:
        user_email = order.customer.email
        if user_email:
            send_mail(
                'Reminder: Last Day to Complete Your Payment',
                'We hope this message finds you well. We want to remind you that you have an outstanding order with us, and tomorrow is the last day to complete your payment.',
                'dummy@ecommerce.com',
                [user_email],
                fail_silently=False,
            )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remind_payments, 'interval', days=1)
    scheduler.start()
