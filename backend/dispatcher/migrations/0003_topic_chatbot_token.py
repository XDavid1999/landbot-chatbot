# Generated by Django 4.2.1 on 2024-12-19 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0002_demo_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='chatbot_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]