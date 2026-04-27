from django.db import migrations


VISIBLE_COMPANY_NAME_BY_USERNAME = {
    "green-tech": "Green Tech",
    "green-tech-solutions": "Green Tech",
    "bright-edge": "Bright Edge",
    "bright-edge-media": "Bright Edge",
    "horizon-retail": "Horizon Retail",
    "connect-care": "Connect Care",
    "finpath": "FinPath",
}


def normalize_visible_employer_company_names(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")

    for profile in Profile.objects.select_related("user").filter(role="employer"):
        visible_name = VISIBLE_COMPANY_NAME_BY_USERNAME.get(profile.user.username)
        if visible_name and profile.company_name != visible_name:
            profile.company_name = visible_name
            profile.save(update_fields=["company_name"])


def reverse_normalize_visible_employer_company_names(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_normalize_remaining_employer_identifiers"),
    ]

    operations = [
        migrations.RunPython(
            normalize_visible_employer_company_names,
            reverse_normalize_visible_employer_company_names,
        ),
    ]
