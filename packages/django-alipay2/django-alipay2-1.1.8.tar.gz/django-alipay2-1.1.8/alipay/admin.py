import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from alipay.alipay import AlipayCertClient, RefundResult
from alipay.models import Refund

logger = logging.getLogger('AlipayAdmin')


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'seller_id', 'sign_type', 'seller_email')


class AlipayPaymentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'out_no', 'no', 'reference_id', 'subject',
                    'amount_total_', 'buyer_email', 'status', 'is_succeed')
    search_fields = ('out_no', 'no', 'buyer_email', 'reference_id')
    list_filter = ('status',)
    raw_id_fields = ('user',)

    def amount_total_(self, obj):
        if obj.refund_total:
            return format_html(f'{obj.amount_total}<span style="color:red;"> -{obj.refund_total}</span>')
        else:
            return obj.amount_total

    def refund_link_(self, obj):
        if obj.refund_total:
            refund_left = obj.amount_total - obj.refund_total
        else:
            refund_left = obj.amount_total

        if not obj.is_succeed() or refund_left <= 0:
            return '-'

        query = {
            '_popup': '1',
            'payment': obj.pk,
            'amount': f'{refund_left:.2f}'
        }

        url_ = reverse('admin:alipay_refund_add') + '?' + urlencode(query)

        return format_html(
            """
            <a id="id_service_due" href="{url}" onchange="javascript:location.reload()"
               class="related-widget-wrapper-link add-related">
               退款
            </a>
            """.format(
                url=url_,
            )
        )

    def get_list_display(self, request):
        can_refund = request.user.is_superuser or request.user.has_perm('alipay.add_refund')
        if can_refund:
            list_display = (*self.list_display, 'refund_link_')
        else:
            list_display = self.list_display

        return list_display


class RefundAdmin(admin.ModelAdmin):
    fields = ('amount', 'payment', 'is_success', 'note')
    list_display = ('amount', 'out_trade_no', 'is_success', 'payment')

    search_fields = ('payment__id',)

    raw_id_fields = ('payment',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk:
            return 'is_success', 'payment', 'amount'
        else:
            return 'is_success',

    def has_delete_permission(self, request, obj=None):
        is_success = obj and obj.is_success
        return not is_success

    def save_model(self, request, obj: Refund, form, change):
        if obj.is_success:
            obj.save()
            return

        client = obj.payment.provider.get_client()

        obj.out_trade_no = obj.out_trade_no or Refund.generate_refund_out_trade_no()

        url = client.create_refund_url(obj.payment.out_no, obj.out_trade_no, str(obj.amount))
        logger.info(f"refund + {url}")

        res = requests.get(url)

        if res.status_code == 200:
            response_dict = res.json()
            logger.info(f"refund <- {response_dict}")
            result = RefundResult.from_response_dict(response_dict)

            obj.is_success = result.is_succeed()
            if obj.is_success:
                obj.payment.refund_total = result.refund_fee
                obj.payment.save()
                msg = None
            else:
                msg = result.msg
                if result.sub_msg:
                    msg = f'{msg} {result.sub_msg}'

        else:
            msg = f'status code {res.status_code}'
            logger.error(f'refund x {res.status_code} {res.text}')

        if msg:
            obj.note = f'{obj.note}\n{msg}'

        obj.save()
