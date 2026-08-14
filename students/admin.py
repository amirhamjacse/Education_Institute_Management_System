# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class SubjectsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
    )
    search_fields = ('name',)


class ClassNameAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
        # 'subjects',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        # 'subjects',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
        # 'subjects',
    )
    search_fields = ('name',)


class SectionClasAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'code',
    )
    search_fields = ('name',)


class ExamAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'exam_yea',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'exam_yea',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'exam_yea',
    )
    search_fields = ('name',)


class ExamYearAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'exam_year',
        'date',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'date',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'exam_year',
        'date',
    )


class ResultInfoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'marks',
        'class_name',
        'subject',
        'section',
        'exam_type',
        'exam_year',
        'student',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'class_name',
        'subject',
        'section',
        'exam_type',
        'exam_year',
        'student',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'marks',
        'class_name',
        'subject',
        'section',
        'exam_type',
        'exam_year',
        'student',
    )
    search_fields = ('name',)


class StudentsInfoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'unique_roll',
        'father_name',
        'mother_name',
        'students_image',
        'date_of_birth',
        'present_address',
        'permanent_address',
        'personal_mobile_number',
        'gurdian_mobile_number',
        'admission_date',
        'gender',
        'class_name',
        'section_class',
        'exam',
        'subjects',
        'user',
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_time',
        'last_updated',
        'deleted_at',
        'date_of_birth',
        'admission_date',
        'class_name',
        'section_class',
        'exam',
        'subjects',
        'id',
        'is_active',
        'is_deleted',
        'created_time',
        'order',
        'display_order',
        'last_updated',
        'deleted_at',
        'name',
        'unique_roll',
        'father_name',
        'mother_name',
        'students_image',
        'date_of_birth',
        'present_address',
        'permanent_address',
        'personal_mobile_number',
        'gurdian_mobile_number',
        'admission_date',
        'gender',
        'class_name',
        'section_class',
        'exam',
        'subjects',
    )
    search_fields = ('name',)
    actions = ['create_login_accounts']

    @admin.action(description='Create login accounts for selected students')
    def create_login_accounts(self, request, queryset):
        from Core.utils import create_logins_for_rows
        created = create_logins_for_rows(
            queryset, prefix='STU', group_name='Student',
            phone_attr='personal_mobile_number',
        )
        if not created:
            self.message_user(request, 'Selected students already have a login account.')
            return
        lines = '; '.join(f'{row}: {uid} / {pw}' for row, uid, pw in created)
        self.message_user(
            request,
            f'Created {len(created)} login(s). Share these securely: {lines}',
        )

class ClassYearAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'class_year',

    )


class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'class_name',
        'section',
        'date',
        'status',
        'marked_by',
        'created_time',
    )
    list_filter = (
        'status',
        'date',
        'class_name',
        'section',
    )
    search_fields = ('student__name', 'student__unique_roll')




def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Subjects, SubjectsAdmin)
_register(models.ClassName, ClassNameAdmin)
_register(models.SectionClas, SectionClasAdmin)
_register(models.ClassYear, ClassYearAdmin)
_register(models.Exam, ExamAdmin)
_register(models.ExamYear, ExamYearAdmin)
_register(models.ResultInfo, ResultInfoAdmin)
_register(models.StudentsInfo, StudentsInfoAdmin)
_register(models.Attendance, AttendanceAdmin)