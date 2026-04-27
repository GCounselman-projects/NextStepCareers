from django.db import migrations


def format_employer_name(value):
    cleaned = " ".join((value or "").replace("_", " ").split())
    if not cleaned:
        return ""
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split())


def normalize_employer_company_names(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")

    for profile in Profile.objects.select_related("user").filter(role="employer"):
        source_value = profile.company_name or profile.user.username
        normalized_name = format_employer_name(source_value)

        if normalized_name and profile.company_name != normalized_name:
            profile.company_name = normalized_name
            profile.save(update_fields=["company_name"])


def reverse_normalize_employer_company_names(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_load_sample_jobs"),
    ]

    operations = [
        migrations.RunPython(
            normalize_employer_company_names,
            reverse_normalize_employer_company_names,
        ),
    ]
