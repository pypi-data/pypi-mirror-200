from django.contrib import admin

from alipay.admin import AlipayPaymentAdmin, RefundAdmin, ProviderAdmin
from alipay.models import AlipayPayment, Refund, Provider

admin.site.register(AlipayPayment, AlipayPaymentAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(Provider, ProviderAdmin)
