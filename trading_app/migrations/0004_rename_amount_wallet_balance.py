# Generated by Django 4.1 on 2024-04-09 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0003_alter_wallet_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='amount',
            new_name='balance',
        ),
    ]
