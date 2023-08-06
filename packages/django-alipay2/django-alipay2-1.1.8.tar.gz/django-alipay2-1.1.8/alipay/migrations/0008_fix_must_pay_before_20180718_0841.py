from datetime import timedelta

from django.db import migrations, models


def fix_must_pay_before(apps, schema_editor):
    AlipayPayment = apps.get_model('alipay', 'AlipayPayment')
    for payment in AlipayPayment.objects.all():
        payment.must_pay_before = payment.created_at + timedelta(minutes=15)
        payment.save()


class Migration(migrations.Migration):
    dependencies = [
        ('alipay', '0007_auto_20180719_1033'),
    ]

    operations = [
        migrations.RunPython(fix_must_pay_before),
        migrations.AlterField(
            model_name='alipaypayment',
            name='must_pay_before',
            field=models.DateTimeField(),
        ),
    ]
