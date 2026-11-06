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

# Routine & Academic Management
@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'period_name', 'start_time', 'end_time', 'is_break')
    list_filter = ('is_break',)

@admin.register(models.TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'class_name', 'section', 'subject', 'academic_year')
    list_filter = ('class_name', 'section', 'subject', 'academic_year')
    search_fields = ('teacher__teachers_name', 'subject__name')

@admin.register(models.ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'section', 'day_of_week', 'time_slot', 'subject', 'teacher', 'room_number')
    list_filter = ('class_name', 'section', 'day_of_week')
    search_fields = ('class_name__name', 'subject__name', 'teacher__teachers_name', 'room_number')

@admin.register(models.ExamAdmitCard)
class ExamAdmitCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'roll_number', 'exam', 'exam_year', 'room_number', 'seat_bench', 'is_approved')
    list_filter = ('exam', 'exam_year', 'is_approved')
    search_fields = ('student__name', 'roll_number')

# Library Management
@admin.register(models.BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'isbn', 'quantity', 'available_copies', 'rack_location')
    list_filter = ('category',)
    search_fields = ('title', 'author', 'isbn')

@admin.register(models.BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'student', 'issue_date', 'due_date', 'return_date', 'status', 'fine_amount')
    list_filter = ('status', 'due_date')
    search_fields = ('book__title', 'student__name')

# Transport & Hostel Management
@admin.register(models.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_number', 'vehicle_model', 'driver_name', 'driver_phone', 'capacity')

@admin.register(models.TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'route_name', 'vehicle', 'start_point', 'end_point', 'monthly_fare')

@admin.register(models.StudentTransport)
class StudentTransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'route', 'pickup_point')

@admin.register(models.Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hostel_type', 'warden_name', 'warden_phone')

@admin.register(models.HostelRoom)
class HostelRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostel', 'room_number', 'capacity', 'occupied_beds', 'cost_per_bed')

@admin.register(models.BedAllocation)
class BedAllocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'room', 'bed_number', 'allocated_date')

# HR & Leave Management
@admin.register(models.LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'days_allowed')

@admin.register(models.LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
    list_filter = ('status', 'leave_type')
