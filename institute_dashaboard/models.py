from django.db import models

# Create your models here.jfd
class Notice_board(models.Model):
    title = models.TextField(max_length=90)
    img_or_pdf = models.FileField(upload_to='Notice_board/', blank=True)
    notice_published_date = models.DateField()
    url_link = models.URLField(blank=True)


class News_headline(models.Model):
    title = models.TextField(max_length=90)
    img_or_pdf = models.FileField(upload_to='News_headline/')
    notice_published_date = models.DateField()
    url_link = models.URLField(blank=True)

class Montri(models.Model):
     title = models.CharField(max_length=90)
     photo = models.FileField(upload_to='Right_side_image_montri/')
     texts = models.TextField(max_length=200)

class Upo_Montri(models.Model):
     title = models.CharField(max_length=90)
     photo = models.FileField(upload_to='Right_side_image_upomontri/')
     texts = models.TextField(max_length=200)
class Sochib(models.Model):
     title = models.CharField(max_length=90)
     photo = models.FileField(upload_to='Right_side_image_sochib/')
     texts = models.TextField(max_length=200)
class DG_or_Chairman(models.Model):
     title = models.CharField(max_length=90)
     photo = models.FileField(upload_to='Right_side_image_DG_or_chairman/')
     texts = models.TextField(max_length=200)

class SineBoard(models.Model):
    title = models.CharField(max_length=90)
    sineboard_photo = models.FileField(upload_to='Sine_board/')
    url_link = models.URLField(blank=True)


class Students_Information(models.Model):
    student_name = models.CharField(max_length=150)
    fathers_name = models.CharField(max_length=150)
    mothers_name = models.CharField(max_length=150)
    unique_roll = models.IntegerField(unique=True,)
    mobile_number = models.IntegerField(default=000)
    seasion = models.IntegerField()
    class_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=10, default='-')
    religion = models.CharField(max_length=50, default='Muslim')
    short_address = models.TextField(default='-')
    students_photo = models.FileField(upload_to='Students_photo/', default='empty-profile.png')

class Teachers_Information(models.Model):
    teachers_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11,)
    email = models.EmailField(max_length=150)
    designation = models.CharField(max_length=150)
    teachers_photo = models.FileField(upload_to='Teachers_Photo/', default='empty-profile.png')

class Other_Employee_Information(models.Model):
    Others_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11,)
    email = models.EmailField(max_length=150)
    designation = models.CharField(max_length=150)
    Others_photo = models.FileField(upload_to='Other_Employee_Photo/')

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    gallery_photo = models.FileField(upload_to='Gallery_Photo/')

class Cultural_Program(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=3000)
    photo_of_culturul_program = models.FileField(upload_to='culturul_program_Photo/')

class Sports(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=3000)
    photo_of_sports = models.FileField(upload_to='sports_Photo/')

class Web_Heading(models.Model):
    name_headline = models.CharField(max_length=70)
    location = models.CharField(max_length=30)
    institute_logo = models.FileField(upload_to='institute_logo/')
    design_and_developer = models.CharField(
        max_length=255, null=True,
        blank=True
    )

class Result(models.Model):
    class_name = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    exam_year = models.IntegerField()
    exam_type = models.CharField(max_length=50)
    unique_roll = models.IntegerField()
    students_name = models.CharField(max_length=50)
    grade_gpa = models.FloatField()
    grade_letter = models.CharField(max_length=2)
    sub1_name = models.CharField(max_length=50, blank=True, null=True)
    sub1_number = models.IntegerField(blank=True, null=True)
    sub2_name = models.CharField(max_length=50, blank=True, null=True)
    sub2_number = models.IntegerField(blank=True, null=True)
    sub3_name = models.CharField(max_length=50, blank=True, null=True)
    sub3_number =models.IntegerField(blank=True, null=True)
    sub4_name = models.CharField(max_length=50, blank=True, null=True)
    sub4_number =models.IntegerField(blank=True, null=True)
    sub5_name = models.CharField(max_length=50, blank=True, null=True)
    sub5_number =models.IntegerField(blank=True, null=True)
    sub6_name = models.CharField(max_length=50, blank=True, null=True)
    sub6_number =models.IntegerField(blank=True, null=True)
    sub7_name = models.CharField(max_length=50, blank=True, null=True)
    sub7_number =models.IntegerField(blank=True, null=True)
    sub8_name = models.CharField(max_length=50, blank=True, null=True)
    sub8_number =models.IntegerField(blank=True, null=True)
    sub9_name = models.CharField(max_length=50,blank=True, null=True)
    sub9_number =models.IntegerField(blank=True, null=True)
    sub10_name = models.CharField(max_length=50, blank=True, null=True)
    sub10_number =models.IntegerField(blank=True, null=True)

class OnlineAdmission(models.Model):
    student_name_bn = models.CharField(max_length=50)
    student_name_en = models.CharField(max_length=50)
    student_father_name_bn = models.CharField(max_length=50)
    student_father_name_en = models.CharField(max_length=50)
    student_mother_name_bn = models.CharField(max_length=50)
    student_mother_name_en = models.CharField(max_length=50)
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender_choise = models.CharField(max_length=80, choices=gender, default='Male')
    student_number = models.CharField(max_length=11)
    gurdian_number = models.CharField(max_length=11)
    date_of_birth = models.DateField()
    present_address = models.TextField()
    admission_fee = models.DecimalField(
        max_digits=10,  # Maximum number of digits
        decimal_places=2,  # Number of decimal places
        default=0.00,  # Default value if not provided
        verbose_name="Admission Fee",  # Optional: a human-readable name for the field
    )
    permanent_address = models.TextField()
    online_admission_pic = models.FileField(upload_to='online_admission/')
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_hold = models.BooleanField(default=False)

class complain(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=11)
    address = models.TextField(blank=True, null=True)
    complain_box = models.TextField()

class Head_Teachers_speach(models.Model):
    speach = models.TextField(max_length=10000)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    picture = models.FileField(upload_to='Head_Teacherspeach/')

class Gallery_Top(models.Model):
    title = models.CharField(max_length=100)
    gallery_photo = models.FileField(upload_to='Heading_slider/')

class Leftside(models.Model):
    amader_dristi = models.TextField()
    amader_lokko =  models.TextField()
    short_porichiti = models.TextField()

class About(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()

class Lokko_uddessho(models.Model):
    lokko = models.TextField()
    uddesho = models.TextField()


class ImportantLink(models.Model):
    name = models.CharField(
        null=True, blank=True,
        max_length=50,
    )
    link = models.URLField(
        blank=True
    )
    icon = models.FileField(
        upload_to='important_link_logo/'
    )



class Transaction(models.Model):
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_id = models.CharField(max_length=15)
    val_id = models.CharField(max_length=75)
    card_type = models.CharField(max_length=150)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_no = models.CharField(max_length=55, null=True)
    bank_tran_id = models.CharField(max_length=155, null=True)
    status = models.CharField(max_length=55)
    tran_date = models.DateTimeField()
    currency = models.CharField(max_length=10)
    card_issuer = models.CharField(max_length=255)
    card_brand = models.CharField(max_length=15)
    card_issuer_country = models.CharField(max_length=55)
    card_issuer_country_code = models.CharField(max_length=55)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=2)
    verify_sign = models.CharField(max_length=155)
    verify_sign_sha2 = models.CharField(max_length=255)
    risk_level = models.CharField(max_length=15)
    risk_title = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name

        
class PaymentGateway(models.Model):
    store_id = models.CharField(
        max_length=500, blank=True, null=True
        )
    store_pass = models.CharField(
        max_length=500, blank=True, null=True
        )
    
    class Meta:
        verbose_name = "Payment Gateway"
        verbose_name_plural = "Payment Gateway"
        
