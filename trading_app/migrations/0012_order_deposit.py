# Generated by Django 4.1 on 2024-04-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0011_alter_order_options_order_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deposit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
