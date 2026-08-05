import io
import random
from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from students.models import (
    ClassYear, ClassName, SectionClas, Session, Subjects,
    Exam, ExamYear, StudentsInfo,
)
from institute_dashaboard.models import (
    Web_Heading, Notice_board, News_headline, Gallery, Event,
    Testimonial, Teachers_Information, Other_Employee_Information,
    SocialMedia,
)

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


CLASS_DEFS = [
    ('Six', '06'),
    ('Seven', '07'),
    ('Eight', '08'),
    ('Nine', '09'),
    ('Ten', '10'),
]
SECTION_DEFS = ['A', 'B']
SUBJECT_DEFS = ['Bangla', 'English', 'Mathematics', 'Science', 'Religion & Moral Education']

MALE_FIRST = [
    'Rakibul', 'Shakib', 'Tanvir', 'Arafat', 'Nayeem', 'Fahim', 'Sabbir',
    'Imran', 'Shahriar', 'Rafiul', 'Mahin', 'Tousif', 'Ridoy', 'Shuvo', 'Anik',
]
FEMALE_FIRST = [
    'Habiba', 'Nusrat', 'Tasnim', 'Sadia', 'Farzana', 'Jannatul', 'Maisha',
    'Rifat', 'Anika', 'Sumaiya', 'Tanjila', 'Mim', 'Israt', 'Nowshin', 'Prapti',
]
SURNAMES = [
    'Islam', 'Rahman', 'Hossain', 'Ahmed', 'Khan', 'Chowdhury',
    'Akter', 'Karim', 'Uddin', 'Alam',
]
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

TEACHERS = [
    ('Md. Abdul Karim', '01711000001', 'headmaster@demo-institute.test', 'Headmaster'),
    ('Md. Nazmul Hasan', '01711000002', 'assthead@demo-institute.test', 'Assistant Headmaster'),
    ('Farida Yeasmin', '01711000003', 'math.teacher@demo-institute.test', 'Senior Teacher - Mathematics'),
    ('Md. Shahin Alam', '01711000004', 'english.teacher@demo-institute.test', 'Senior Teacher - English'),
    ('Nasrin Sultana', '01711000005', 'science.teacher@demo-institute.test', 'Science Teacher'),
    ('Md. Kamrul Hasan', '01711000006', 'bangla.teacher@demo-institute.test', 'Bangla Teacher'),
    ('Md. Jahangir Alam', '01711000007', 'pe.teacher@demo-institute.test', 'Physical Education Teacher'),
    ('Sharmin Akter', '01711000008', 'ict.teacher@demo-institute.test', 'Computer / ICT Teacher'),
]
STAFF = [
    ('Md. Aynal Haque', '01811000001', 'office@demo-institute.test', 'Office Assistant'),
    ('Rehana Begum', '01811000002', 'accounts@demo-institute.test', 'Accountant'),
    ('Md. Selim Mia', '01811000003', 'librarian@demo-institute.test', 'Librarian'),
    ('Md. Boshir Uddin', '01811000004', 'security@demo-institute.test', 'Security Guard'),
]


class Command(BaseCommand):
    help = (
        'Seed the database with demo data (classes, sections, students, '
        'teachers, staff, notices, news, events, testimonials, gallery, '
        'placeholder logo/photos) for local development and demos.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete previously seeded demo records before creating new ones.'
        )
        parser.add_argument(
            '--per-section', type=int, default=6,
            help='Number of demo students to create per class/section (default: 6).'
        )
        parser.add_argument(
            '--no-images', action='store_true',
            help='Skip generating placeholder photos/logo/gallery images; seed data-only records.'
        )

    def handle(self, *args, **options):
        self.use_images = HAS_PIL and not options['no_images']
        if options['no_images']:
            self.stdout.write(self.style.WARNING(
                'Skipping placeholder images (--no-images).'
            ))
        elif not HAS_PIL:
            self.stdout.write(self.style.WARNING(
                'Pillow not available - placeholder images will be skipped.'
            ))

        if options['flush']:
            self.flush_demo_data()

        with transaction.atomic():
            self.seed_web_heading()
            class_year = self.seed_class_year()
            self.seed_sessions()
            classes = self.seed_classes(class_year)
            sections = self.seed_sections(classes)
            self.seed_subjects(classes)
            self.seed_exam()
            total_students = self.seed_students(
                classes, sections, options['per_section']
            )
            self.seed_teachers()
            self.seed_staff()
            self.seed_notices()
            self.seed_news()
            self.seed_events()
            self.seed_testimonials()
            self.seed_gallery()
            self.seed_social_media()

        self.stdout.write(self.style.SUCCESS(
            f'Demo data seeded: {len(classes)} classes, '
            f'{len(classes) * len(SECTION_DEFS)} sections, '
            f'{total_students} students, {len(TEACHERS)} teachers, '
            f'{len(STAFF)} staff members.'
        ))

    # ------------------------------------------------------------------
    # cleanup
    # ------------------------------------------------------------------
    def flush_demo_data(self):
        StudentsInfo.objects.all().delete()
        Subjects.objects.all().delete()
        SectionClas.objects.all().delete()
        ClassName.objects.all().delete()
        ClassYear.objects.all().delete()
        Session.objects.all().delete()
        Exam.objects.all().delete()
        ExamYear.objects.all().delete()
        Teachers_Information.objects.all().delete()
        Other_Employee_Information.objects.all().delete()
        Notice_board.objects.all().delete()
        News_headline.objects.all().delete()
        Gallery.objects.all().delete()
        Event.objects.all().delete()
        Testimonial.objects.all().delete()
        SocialMedia.objects.all().delete()
        Web_Heading.objects.all().delete()
        self.stdout.write(self.style.WARNING('Previous demo data flushed.'))

    # ------------------------------------------------------------------
    # image helpers
    # ------------------------------------------------------------------
    # A valid, near-empty 1x1 PNG. Used in --no-images mode so FileFields that
    # other templates dereference with `.url` unguarded (gallery, staff/teacher
    # photos, news images) don't raise ValueError on an empty file.
    _TINY_PNG = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )

    def _placeholder_image(self, text, bg, size=(400, 400)):
        if not self.use_images:
            return ContentFile(self._TINY_PNG, name='placeholder.png')
        img = Image.new('RGB', size, color=bg)
        draw = ImageDraw.Draw(img)
        font_size = int(min(size) * 0.28)
        try:
            font = ImageFont.truetype('DejaVuSans-Bold.ttf', font_size)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((size[0] - w) / 2 - bbox[0], (size[1] - h) / 2 - bbox[1]),
            text, fill='white', font=font,
        )
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return ContentFile(buf.read(), name=f'{text.replace(" ", "_")}.png')

    def _initials(self, name):
        parts = [p for p in name.replace('Md.', '').replace('Mst.', '').split() if p]
        return ''.join(p[0] for p in parts[:2]).upper() or 'NA'

    # ------------------------------------------------------------------
    # seeders
    # ------------------------------------------------------------------
    def seed_web_heading(self):
        if Web_Heading.objects.exists():
            return
        heading = Web_Heading(
            name_headline='Demo Ideal Institute',
            location='Dhaka, Bangladesh',
            design_and_developer='Institute Management System',
        )
        logo = self._placeholder_image('DII', (8, 114, 67), size=(300, 300))
        if logo:
            heading.institute_logo.save(logo.name, logo, save=False)
        heading.save()

    def seed_class_year(self):
        class_year, _ = ClassYear.objects.get_or_create(class_year='2026')
        return class_year

    def seed_sessions(self):
        for name in ['2024-2025', '2025-2026']:
            Session.objects.get_or_create(name=name)

    def seed_classes(self, class_year):
        classes = []
        for name, code in CLASS_DEFS:
            cls, _ = ClassName.objects.get_or_create(
                name=name, defaults={'code': code, 'class_nm': class_year}
            )
            classes.append(cls)
        return classes

    def seed_sections(self, classes):
        sections = {}
        for cls in classes:
            sections[cls.id] = []
            for sec_name in SECTION_DEFS:
                section, _ = SectionClas.objects.get_or_create(
                    class_nm=cls, name=sec_name,
                    defaults={'code': f'{cls.code}{sec_name}'}
                )
                sections[cls.id].append(section)
        return sections

    def seed_subjects(self, classes):
        for cls in classes:
            for i, subj in enumerate(SUBJECT_DEFS, start=1):
                Subjects.objects.get_or_create(
                    name=subj, class_nm=cls,
                    defaults={'code': f'{cls.code}{i:02d}'}
                )

    def seed_exam(self):
        exam_year, _ = ExamYear.objects.get_or_create(
            exam_year='2026', defaults={'date': date(2026, 12, 1)}
        )
        exam, _ = Exam.objects.get_or_create(
            name='Annual Examination', exam_yea=exam_year
        )
        return exam

    def seed_students(self, classes, sections, per_section):
        total = 0
        for cls_index, cls in enumerate(classes):
            base_age = 11 + cls_index
            for section in sections[cls.id]:
                for i in range(1, per_section + 1):
                    is_male = (total % 2 == 0)
                    first = random.choice(MALE_FIRST if is_male else FEMALE_FIRST)
                    surname = random.choice(SURNAMES)
                    name = f"{'Md. ' if is_male else ''}{first} {surname}"
                    roll = f"{cls.code}{section.name}{i:02d}"

                    if StudentsInfo.objects.filter(unique_roll=roll).exists():
                        continue

                    dob = date(2026 - base_age, random.randint(1, 12), random.randint(1, 28))
                    student = StudentsInfo(
                        name=name,
                        unique_roll=roll,
                        father_name=f"Md. {random.choice(SURNAMES)} {random.choice(SURNAMES)}",
                        mother_name=f"Mst. {random.choice(SURNAMES)} {random.choice(SURNAMES)}",
                        date_of_birth=dob,
                        present_address='House 12, Road 5, Mirpur, Dhaka',
                        permanent_address='Village Road, Savar, Dhaka',
                        personal_mobile_number=f"017{random.randint(10000000, 99999999)}",
                        blood_group=random.choice(BLOOD_GROUPS),
                        gurdian_mobile_number=f"018{random.randint(10000000, 99999999)}",
                        admission_date=date(2026 - base_age + 6, 1, 10),
                        gender='male' if is_male else 'female',
                        relegion='islam',
                        session='2025-2026',
                        class_name=cls,
                        section_class=section,
                    )
                    photo = self._placeholder_image(
                        self._initials(name),
                        (8, 114, 67) if is_male else (194, 47, 93),
                        size=(300, 300),
                    )
                    if photo:
                        student.students_image.save(photo.name, photo, save=False)
                    student.save()
                    total += 1
        return total

    def seed_teachers(self):
        for name, phone, email, designation in TEACHERS:
            if Teachers_Information.objects.filter(email=email).exists():
                continue
            teacher = Teachers_Information(
                teachers_name=name, phone_number=phone,
                email=email, designation=designation,
            )
            photo = self._placeholder_image(self._initials(name), (40, 76, 120), size=(300, 300))
            if photo:
                teacher.teachers_photo.save(photo.name, photo, save=False)
            teacher.save()

    def seed_staff(self):
        for name, phone, email, designation in STAFF:
            if Other_Employee_Information.objects.filter(email=email).exists():
                continue
            staff = Other_Employee_Information(
                Others_name=name, phone_number=phone,
                email=email, designation=designation,
            )
            photo = self._placeholder_image(self._initials(name), (100, 100, 100), size=(300, 300))
            if photo:
                staff.Others_photo.save(photo.name, photo, save=False)
            staff.save()

    def seed_notices(self):
        titles = [
            'Annual Examination Routine 2026 Published',
            'Winter Vacation Notice',
            'Admission Circular for New Session 2026-2027',
            'Parent-Teacher Meeting Schedule',
            'Sports Day Announcement',
        ]
        today = date.today()
        for i, title in enumerate(titles):
            Notice_board.objects.get_or_create(
                title=title,
                defaults={'notice_published_date': today - timedelta(days=i * 3)}
            )

    def seed_news(self):
        items = [
            'Institute Achieves 100% Pass Rate in Board Exams',
            'New Science Lab Inaugurated',
            'Students Win District Debate Competition',
        ]
        today = date.today()
        for i, title in enumerate(items):
            if News_headline.objects.filter(title=title).exists():
                continue
            news = News_headline(
                title=title, notice_published_date=today - timedelta(days=i * 5)
            )
            img = self._placeholder_image(f'NEWS {i + 1}', (194, 47, 93), size=(500, 300))
            if img:
                news.img_or_pdf.save(img.name, img, save=False)
            news.save()

    def seed_events(self):
        events = [
            ('Annual Sports Day', 40),
            ('Science Fair', 25),
            ('Cultural Program', 60),
        ]
        today = date.today()
        for title, days_ahead in events:
            Event.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Join us for the {title.lower()} at the institute campus.',
                    'event_date': today + timedelta(days=days_ahead),
                    'location': 'Main Campus Ground',
                    'is_upcoming': True,
                }
            )

    def seed_testimonials(self):
        testimonials = [
            ('Abdur Rahman', 'Guardian', 'A wonderful institute with dedicated teachers who genuinely care about every student.'),
            ('Nasima Begum', 'Guardian', "My daughter's results and confidence have improved a lot since she joined."),
            ('Md. Kamal Hossain', 'Alumnus', 'The discipline and quality education I received here shaped my career.'),
        ]
        for name, designation, message in testimonials:
            Testimonial.objects.get_or_create(
                name=name, defaults={'designation': designation, 'message': message}
            )

    def seed_gallery(self):
        for i in range(1, 7):
            title = f'Campus Moment {i}'
            if Gallery.objects.filter(title=title).exists():
                continue
            gallery = Gallery(title=title)
            img = self._placeholder_image(f'IMG {i}', (87, 114, 67), size=(400, 300))
            if img:
                gallery.gallery_photo.save(img.name, img, save=False)
            gallery.save()

    def seed_social_media(self):
        socials = [
            ('Facebook', 'https://facebook.com/demo-institute', 'bi-facebook'),
            ('YouTube', 'https://youtube.com/@demo-institute', 'bi-youtube'),
            ('WhatsApp', 'https://wa.me/8801700000000', 'bi-whatsapp'),
        ]
        for platform, url, icon in socials:
            SocialMedia.objects.get_or_create(
                platform=platform, defaults={'url': url, 'icon_class': icon}
            )
