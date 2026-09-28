from django.db import migrations

EDITOR_GROUP = "Editor"


def create_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=EDITOR_GROUP)


def delete_editor_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=EDITOR_GROUP).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("main", "0007_music_starred_by"),
    ]

    operations = [
        migrations.RunPython(create_editor_group, delete_editor_group),
    ]
