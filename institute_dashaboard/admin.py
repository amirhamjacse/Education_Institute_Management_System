from django.contrib import admin
from .models import (
    Lokko_uddessho, About,
    Leftside,Gallery_Top, Head_Teachers_speach,complain, 
    OnlineAdmission, Notice_board, Result,  News_headline, Montri, 
    Sochib, DG_or_Chairman, Upo_Montri, SineBoard,Students_Information, 
    Teachers_Information, Other_Employee_Information, Gallery,
    Cultural_Program, Sports, Web_Heading, ImportantLink, Transaction, PaymentGateway,
    Event, Testimonial, Download, SocialMedia, SiteMeta, TeacherAttendance
)


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'date', 'status', 'marked_by', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('teacher__teachers_name',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_no', 'amount',  'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('currency', 'status')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PaymentGateway)



#Register your models here.
@admin.register(Notice_board)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id','title','img_or_pdf', 'notice_published_date', 'url_link']

@admin.register(News_headline)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id','title','img_or_pdf', 'url_link']

@admin.register(Montri)
class RightSidemontriAdmin(admin.ModelAdmin):
    list_display = ['id','title','photo', 'texts']
@admin.register(Upo_Montri)
class RightSideupmontriAdmin(admin.ModelAdmin):
    list_display = ['id','title','photo', 'texts']
@admin.register(Sochib)
class RightSidesochibAdmin(admin.ModelAdmin):
    list_display = ['id','title','photo', 'texts']
@admin.register(DG_or_Chairman)
class RightSideteacherAdmin(admin.ModelAdmin):
    list_display = ['id','title','photo', 'texts']

@admin.register(SineBoard)
class SineBoardAdmin(admin.ModelAdmin):
    list_display = ['id','title','sineboard_photo', 'url_link']


@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ['id','name','link', 'icon']


@admin.register(Students_Information)
class Students_InformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_name','fathers_name', 'mothers_name', 'unique_roll', 'mobile_number', 'seasion', 'class_name', 'date_of_birth', 'blood_group', 'religion', 'short_address', 'students_photo']

@admin.register(Teachers_Information)
class Teachers_InformationAdmin(admin.ModelAdmin):
    list_display = ['id','teachers_name','phone_number', 'email', 'designation', 'teachers_photo', 'user']
    actions = ['create_login_accounts']

    @admin.action(description='Create login accounts for selected teachers')
    def create_login_accounts(self, request, queryset):
        from Core.utils import create_logins_for_rows
        created = create_logins_for_rows(
            queryset, prefix='TCH', group_name='Teacher',
            phone_attr='phone_number',
        )
        if not created:
            self.message_user(request, 'Selected teachers already have a login account.')
            return
        lines = '; '.join(f'{row}: {uid} / {pw}' for row, uid, pw in created)
        self.message_user(
            request,
            f'Created {len(created)} login(s). Share these securely: {lines}',
        )

@admin.register(Other_Employee_Information)
class Other_Employee_InformationAdmin(admin.ModelAdmin):
    list_display = ['id','Others_name','phone_number', 'email', 'designation', 'Others_photo', 'user']
    actions = ['create_login_accounts']

    @admin.action(description='Create login accounts for selected staff')
    def create_login_accounts(self, request, queryset):
        from Core.utils import create_logins_for_rows
        created = create_logins_for_rows(
            queryset, prefix='STF', group_name='Staff',
            phone_attr='phone_number',
        )
        if not created:
            self.message_user(request, 'Selected staff already have a login account.')
            return
        lines = '; '.join(f'{row}: {uid} / {pw}' for row, uid, pw in created)
        self.message_user(
            request,
            f'Created {len(created)} login(s). Share these securely: {lines}',
        )

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id','title','gallery_photo']

@admin.register(Gallery_Top)
class GallertpyAdmin(admin.ModelAdmin):
    list_display = ['id','title','gallery_photo']

@admin.register(Cultural_Program)
class Cultural_ProgramAdmin(admin.ModelAdmin):
    list_display = ['id','title','details', 'photo_of_culturul_program']

@admin.register(Sports)
class SportsAdmin(admin.ModelAdmin):
    list_display = ['id','title','details', 'photo_of_sports']

@admin.register(Web_Heading)
class Web_HeadingAdmin(admin.ModelAdmin):
    list_display = ['id','name_headline','location', 'institute_logo']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['id' ,'students_name', 'class_name', 'session', 'unique_roll', 'exam_year', 'exam_type', 'grade_gpa', 'grade_letter', 'sub1_name', 'sub1_number', 'sub2_name', 'sub2_number','sub3_name', 'sub3_number','sub4_name', 'sub4_number','sub5_name', 'sub5_number','sub6_name', 'sub6_number','sub7_name', 'sub7_number','sub8_name', 'sub8_number','sub9_name', 'sub9_number', 'sub10_name', 'sub10_number',  ]

@admin.register(OnlineAdmission)
class OnlineadmiAdmin(admin.ModelAdmin):
    list_display = ['id','student_name_en','student_father_name_bn', 'student_father_name_en', 'student_mother_name_bn', 'student_mother_name_en', 'gender_choise', 'student_number', 'gurdian_number', 'date_of_birth', 'present_address', 'permanent_address', 'online_admission_pic' ]

@admin.register(complain)
class complainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile', 'address', 'complain_box' ]

@admin.register(Head_Teachers_speach)
class SpeachAdmin(admin.ModelAdmin):
    list_display = ['id', 'speach', 'name', 'designation', 'picture']

@admin.register(Leftside)
class LeftsideAdmin(admin.ModelAdmin):
    list_display = ['id', 'amader_dristi', 'amader_lokko', 'short_porichiti']
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'details']
@admin.register(Lokko_uddessho)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['id', 'lokko', 'uddesho']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'is_upcoming']
    list_filter = ['is_upcoming', 'event_date']
    search_fields = ['title']
    date_hierarchy = 'event_date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'message']

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title']

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active']
    list_filter = ['is_active']

@admin.register(SiteMeta)
class SiteMetaAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'meta_description']
