# Generated by Django 2.1.5 on 2019-03-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0020_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmessage',
            name='expired_reminder',
            field=models.TextField(default='Hello {}, Your subscription has now been expired if you wish to still renew please proceed to http://announceus.io'),
        ),
        migrations.AddField(
            model_name='botmessage',
            name='finely_reminder',
            field=models.TextField(default='Hello {}, This is your Final Reminder your membership expires in 24 hours. To renew your membership use !renew command.'),
        ),
        migrations.AddField(
            model_name='botmessage',
            name='first_reminder',
            field=models.TextField(default='Hello {}, This is your 1st reminder that your Premium Membership expires in 7 days. To renew your membership use !renew command.'),
        ),
        migrations.AddField(
            model_name='botmessage',
            name='join_message',
            field=models.TextField(default='Hello, {} Welcome to announceus.io discord server. Please use following Commands:\n            {}\n'),
        ),
        migrations.AddField(
            model_name='botmessage',
            name='second_reminder',
            field=models.TextField(default='Hello {}, This is your 2nd reminder that your Premium Membership expires in 3 days. To renew your membership use !renew command.'),
        ),
    ]
