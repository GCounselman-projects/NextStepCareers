import re

from django.db import migrations


def format_employer_name(value):
    cleaned = re.sub(r"[_-]+", " ", value or "")
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return ""
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split())


def username_slug(value):
    return "-".join(format_employer_name(value).lower().split())


def build_unique_username(User, desired_username, current_user_id):
    candidate = desired_username
    suffix = 2

    while User.objects.exclude(pk=current_user_id).filter(username=candidate).exists():
        candidate = f"{desired_username}-{suffix}"
        suffix += 1

    return candidate


def normalize_remaining_employer_identifiers(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("core", "Profile")
    Notification = apps.get_model("core", "Notification")

    employer_profiles = list(Profile.objects.select_related("user").filter(role="employer"))

    for profile in employer_profiles:
        original_username = profile.user.username
        normalized_name = format_employer_name(profile.company_name or original_username)

        if normalized_name and profile.company_name != normalized_name:
            profile.company_name = normalized_name
            profile.save(update_fields=["company_name"])

        if "_" in original_username:
            desired_username = username_slug(normalized_name or original_username)
            unique_username = build_unique_username(User, desired_username, profile.user_id)
            if unique_username != original_username:
                profile.user.username = unique_username
                profile.user.save(update_fields=["username"])

            for notification in Notification.objects.filter(text__contains=original_username):
                notification.text = notification.text.replace(original_username, normalized_name)
                notification.save(update_fields=["text"])


def reverse_normalize_remaining_employer_identifiers(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_normalize_employer_company_names"),
    ]

    operations = [
        migrations.RunPython(
            normalize_remaining_employer_identifiers,
            reverse_normalize_remaining_employer_identifiers,
        ),
    ]
