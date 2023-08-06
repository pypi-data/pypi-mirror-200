from datetime import timedelta
from unittest.mock import Mock

import pytz
from django.test import TestCase
from django.utils import timezone

from alipay.models import AlipayPayment
from alipay.signals import payment_succeed


class AlipayPaymentTest(TestCase):
    def test_signal_payment_succeed(self):
        payment = AlipayPayment.objects.create(
            out_no='123',
            subject='充值',
            body='1年365元',
            amount_total=0.01,
        )

        mock = Mock()
        payment_succeed.connect(mock)

        payment.status = AlipayPayment.TRADE_SUCCESS
        payment.save()
        self.assertEqual(mock.call_count, 1)

        payment.status = AlipayPayment.TRADE_FINISHED
        payment.save()
        self.assertEqual(mock.call_count, 1, '只有从未成功切换成成功的时候才抛signal')

    def test_must_pay_before(self):
        payment = AlipayPayment.objects.create(
            out_no='out-no',
            subject='subject',
            body='body',
            amount_total=0.01,
        )
        self.assertEqual(payment.expire, '15m', '默认15分钟')
        self.assertAlmostEqual((payment.must_pay_before - payment.created_at).total_seconds(), 900.0, 2, '预期支付时间是15分钟后')

        payment.expire = '1c'
        payment.created_at = payment.created_at.replace(hour=11, minute=59, second=59, microsecond=0)
        payment.created_at = payment.created_at.replace(tzinfo=pytz.timezone('UTC'))
        payment.must_pay_before = None
        payment.save()

        self.assertEqual(
            (payment.must_pay_before - payment.created_at).total_seconds(),
            4 * 3600,
            '预期支付时间是4小时后'
        )

    def test_expire_delta(self):
        created_at = timezone.now()
        expire = "20m"
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(minutes=20), '20分钟')

        expire = "3h"
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(hours=3), '3小时')

        expire = "2d"
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(days=2), '2天')

        created_at = created_at.replace(
            hour=11, minute=59, second=59, microsecond=0,
            tzinfo=pytz.timezone('Asia/Shanghai')
        )
        expire = '1c'
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(hours=12),
                         '预期支付时间是北京时间晚上11:59:59')

        created_at = created_at.replace(
            hour=11, minute=59, second=59, microsecond=0,
            tzinfo=pytz.timezone('Etc/GMT-11')  # 东11区
        )
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(hours=15),
                         '预期支付时间是23-(11-11+8)%24=15小时')

        created_at = created_at.replace(
            hour=11, minute=59, second=59, microsecond=0,
            tzinfo=pytz.timezone('Etc/GMT+11')  # 西11区
        )
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(hours=17),
                         '预期支付时间是23-(11+11+8)%24=17小时')

        created_at = created_at.replace(
            hour=11, minute=59, second=59, microsecond=0,
            tzinfo=pytz.timezone('utc')  # 西11区
        )
        self.assertEqual(AlipayPayment.get_expire_delta(expire, created_at), timedelta(hours=4),
                         '预期支付时间是23-(11+8)%24=4小时')

        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire should between 1m and 10d"):
            AlipayPayment.get_expire_delta('11d', created_at)

        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire should between 1m and 10d"):
            AlipayPayment.get_expire_delta('0m', created_at)

        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire not valid"):
            AlipayPayment.get_expire_delta('-1m', created_at)

        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire not valid"):
            AlipayPayment.get_expire_delta('2md', created_at)
        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire not valid"):
            AlipayPayment.get_expire_delta('2s', created_at)
        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire not valid"):
            AlipayPayment.get_expire_delta(' 2m', created_at)
        with self.assertRaisesMessage(AssertionError, "AlipayPayment.expire not valid"):
            AlipayPayment.get_expire_delta('m', created_at)
