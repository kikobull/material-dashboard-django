# Generated by Django 3.2.6 on 2023-03-25 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode', '0004_qrcodes_enable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodes',
            name='expiry_dt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='notes',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
