import django.dispatch

if getattr(django, '__version__') >= '4.0':
    payment_succeed = django.dispatch.Signal()
else:
    payment_succeed = django.dispatch.Signal(providing_args=['instance'])
