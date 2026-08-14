import secrets
import string


def generate_temp_password(length=10):
    """Random temporary login password (letters + digits)."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_prefixed_user_id(prefix):
    """Sequential login id like TCH00007, scoped to the given prefix."""
    from Core.models import User
    count = User.objects.filter(user_id__startswith=prefix).count() + 1
    return f"{prefix}{count:05d}"


def create_logins_for_rows(rows, prefix, group_name, phone_attr='phone_number'):
    """Create a login account for each row in `rows` that doesn't have one.

    Each row must have a `user` FK and the given phone attribute. Returns a
    list of (row, user_id, temp_password) for rows that got a new account.
    """
    from django.contrib.auth.models import Group
    from Core.models import User

    group, _ = Group.objects.get_or_create(name=group_name)
    created = []
    for row in rows:
        if row.user_id:
            continue
        user_id = generate_prefixed_user_id(prefix)
        temp_password = generate_temp_password()
        user = User.objects.create_user(
            user_id=user_id, password=temp_password,
            phone=getattr(row, phone_attr, None),
        )
        row.user = user
        row.save(update_fields=['user'])
        user.groups.add(group)
        created.append((row, user_id, temp_password))
    return created
