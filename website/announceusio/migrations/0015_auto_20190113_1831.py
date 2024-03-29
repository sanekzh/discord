# Generated by Django 2.1.5 on 2019-01-13 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0014_sitesettings_member_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invite',
        ),
        migrations.AddField(
            model_name='member',
            name='is_invited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='message_body',
            field=models.TextField(default='{invite_url}', help_text='You must set {invite_url} in message body!'),
        ),
    ]
