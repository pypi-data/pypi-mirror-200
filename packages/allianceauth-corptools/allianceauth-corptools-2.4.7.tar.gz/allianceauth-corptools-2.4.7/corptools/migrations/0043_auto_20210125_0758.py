# Generated by Django 3.1.1 on 2021-01-25 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0042_remove_skilllist_eft'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporationaudit',
            name='cache_expire_wallet',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='corporationaudit',
            name='last_update_wallet',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
