from django.db import migrations


def migrate_data(apps, schema_editor):
    Topic = apps.get_model("dispatcher", "Topic")
    Notification = apps.get_model("dispatcher", "Notification")

    # Create Demo Sales Topic and Notification
    sales = Topic.objects.create(
        name="Demo sales", description="This is a demo sales service"
    )
    sales_notification = Notification.objects.create(
        method="Email",
        config={"recipient_list": ["test@test.test", "test2@test.test"]},
    )
    sales.notification = sales_notification
    sales.save()

    # Create Demo Pricing Topic and Notification
    pricing = Topic.objects.create(
        name="Demo pricing", description="This is a demo pricing service"
    )
    pricing_notification = Notification.objects.create(
        method="Slack",
        config={"channel": "#pricing"},
    )
    pricing.notification = pricing_notification
    pricing.save()

    # Create Demo HR Topic and Notification
    human_resources = Topic.objects.create(
        name="Demo HR", description="This is a demo HR service"
    )
    hr_notification = Notification.objects.create(
        method="Telegram",
        config={"chat_id": "123456789"},
    )
    human_resources.notification = hr_notification
    human_resources.save()


def reverse_data(apps, schema_editor):
    Topic = apps.get_model("dispatcher", "Topic")

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
