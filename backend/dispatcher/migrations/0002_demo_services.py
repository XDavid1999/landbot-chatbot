from django.db import migrations
from dispatcher.models import Topic, Notification


def migrate_data(apps, schema_editor):
    sales = Topic.objects.create(
        name="Demo sales", description="This is a demo sales service"
    )
    sales_notification = Notification.objects.create(
        method=Notification.EMAIL,
        config={"recipient_list": ["test@test", "test2@test"]},
    )
    sales.notification = sales_notification
    sales.save()

    pricing = Topic.objects.create(
        name="Demo pricing", description="This is a demo pricing service"
    )
    pricing_notification = Notification.objects.create(
        method=Notification.SLACK,
        config={"channel": "#pricing"},
    )
    pricing.notification = pricing_notification
    pricing.save()

    human_resources = Topic.objects.create(
        name="Demo HR", description="This is a demo HR service"
    )
    hr_notification = Notification.objects.create(
        method=Notification.TELEGRAM,
        config={"chat_id": "123456789"},
    )
    human_resources.notification = hr_notification
    human_resources.save()


def reverse_data(apps, schema_editor):
    topics = Topic.objects.filter(name__in=["Demo sales", "Demo pricing", "Demo HR"])
    for topic in topics:
        if topic.notification:
            topic.notification.delete()
        topic.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("dispatcher", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_data, reverse_data),
    ]
