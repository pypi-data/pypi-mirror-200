# Generated by Django 3.2.5 on 2021-07-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corptools', '0052_charactercontact_charactercontactlabel_corporationcontact_corporationcontactlabel'),
    ]

    operations = [
        migrations.AddField(
            model_name='characteraudit',
            name='last_update_contacts',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
