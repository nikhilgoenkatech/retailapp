# Generated by Django 2.2.6 on 2019-10-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='first_name',
            field=models.CharField(default='t', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='last_name',
            field=models.CharField(default='t', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(default='t', max_length=30),
            preserve_default=False,
        ),
    ]
