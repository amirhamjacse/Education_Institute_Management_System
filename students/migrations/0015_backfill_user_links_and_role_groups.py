from django.db import migrations


def backfill_and_seed(apps, schema_editor):
    StudentsInfo = apps.get_model('students', 'StudentsInfo')
    User = apps.get_model('Core', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Backfill the FK using the pre-existing implicit convention
    # (unique_roll == user_id) for students created before this link existed.
    for student in StudentsInfo.objects.filter(
        user__isnull=True
    ).exclude(unique_roll__isnull=True).exclude(unique_roll=''):
        user = User.objects.filter(user_id=student.unique_roll).first()
        if user:
            student.user = user
            student.save(update_fields=['user'])

    def get_perm(app_label, codename):
        return Permission.objects.filter(
            content_type__app_label=app_label, codename=codename
        ).first()

    student_group, _ = Group.objects.get_or_create(name='Student')
    student_perms = [get_perm('students', 'view_resultinfo')]
    student_group.permissions.set([p for p in student_perms if p])

    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    teacher_perms = [
        get_perm('students', 'add_resultinfo'),
        get_perm('students', 'change_resultinfo'),
        get_perm('students', 'view_resultinfo'),
        get_perm('students', 'add_attendance'),
        get_perm('students', 'view_attendance'),
    ]
    teacher_group.permissions.set([p for p in teacher_perms if p])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_studentsinfo_user'),
        ('institute_dashaboard', '0033_other_employee_information_user_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(backfill_and_seed, noop_reverse),
    ]
