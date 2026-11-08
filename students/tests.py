import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from students.models import (
    ClassYear, ClassName, SectionClas, Subjects, Exam, ExamYear, StudentsInfo,
    TimeSlot, TeacherAssignment, ClassRoutine, ExamAdmitCard,
    BookCategory, Book, BookIssue,
    Vehicle, TransportRoute, StudentTransport,
    Hostel, HostelRoom, BedAllocation,
    LeaveType, LeaveApplication
)
from institute_dashaboard.models import OnlineAdmission, Teachers_Information

User = get_user_model()


class AcademicAndOperationsBaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(
            user_id='admin_test',
            email='admin@test.com',
            password='password123'
        )
        self.client.force_login(self.staff_user)

        # Base academic setup
        self.class_year = ClassYear.objects.create(class_year='2026')
        self.class_name = ClassName.objects.create(name='Class Nine', code='09', class_nm=self.class_year)
        self.section = SectionClas.objects.create(class_nm=self.class_name, name='A', code='09A')
        self.subject = Subjects.objects.create(name='Physics', code='0901', class_nm=self.class_name)

        self.student = StudentsInfo.objects.create(
            name='Test Student',
            unique_roll='09A01',
            father_name='Father Name',
            mother_name='Mother Name',
            date_of_birth=datetime.date(2010, 1, 1),
            personal_mobile_number='01700000001',
            gurdian_mobile_number='01800000001',
            class_name=self.class_name,
            section_class=self.section,
            gender='male',
            relegion='islam',
            session='2025-2026'
        )

        self.teacher = Teachers_Information.objects.create(
            teachers_name='Test Teacher',
            phone_number='01711223344',
            email='teacher@test.com',
            designation='Lecturer'
        )


class RoutineTests(AcademicAndOperationsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.time_slot = TimeSlot.objects.create(
            period_name='1st Period',
            start_time=datetime.time(9, 0),
            end_time=datetime.time(9, 45),
            is_break=False
        )

    def test_routine_view_and_matrix(self):
        # Create a routine entry
        routine = ClassRoutine.objects.create(
            class_name=self.class_name,
            section=self.section,
            subject=self.subject,
            teacher=self.teacher,
            time_slot=self.time_slot,
            day_of_week='Monday',
            room_number='Room 101'
        )

        # GET routine view
        response = self.client.get(
            reverse('students:students_routine') + f'?class_id={self.class_name.id}&section_id={self.section.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Class Nine')
        self.assertContains(response, 'Physics')

    def test_create_and_delete_routine_slot(self):
        # Post new routine slot
        post_data = {
            'action': 'add_slot',
            'class_id': self.class_name.id,
            'section_id': self.section.id,
            'time_slot': self.time_slot.id,
            'day': 'Tuesday',
            'subject': self.subject.id,
            'teacher': self.teacher.id,
            'room_number': 'Room 102',
        }
        res = self.client.post(reverse('students:students_routine'), post_data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            ClassRoutine.objects.filter(
                class_name=self.class_name,
                section=self.section,
                day_of_week='Tuesday'
            ).exists()
        )

        slot = ClassRoutine.objects.get(day_of_week='Tuesday')
        del_res = self.client.post(reverse('students:delete_routine_slot', args=[slot.id]))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(ClassRoutine.objects.filter(id=slot.id).exists())


class LibraryTests(AcademicAndOperationsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = BookCategory.objects.create(name='Science', code='SCI')
        self.book = Book.objects.create(
            title='Intro to Physics',
            author='Isaac Newton',
            category=self.category,
            quantity=5,
            available_copies=5
        )

    def test_book_catalog_view(self):
        res = self.client.get(reverse('students:library_catalog'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Intro to Physics')

    def test_book_issue_and_return_lifecycle(self):
        # Issue book to student
        issue_res = self.client.post(reverse('students:library_issues'), {
            'book': self.book.id,
            'student': self.student.id,
            'days': 10
        })
        self.assertEqual(issue_res.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 4)

        issue = BookIssue.objects.get(book=self.book, student=self.student)
        self.assertEqual(issue.status, 'ISSUED')

        # Return the book
        return_res = self.client.post(reverse('students:library_return', args=[issue.id]))
        self.assertEqual(return_res.status_code, 302)

        issue.refresh_from_db()
        self.book.refresh_from_db()
        self.assertEqual(issue.status, 'RETURNED')
        self.assertEqual(self.book.available_copies, 5)

    def test_my_books_view(self):
        # Link user to student profile
        student_user = User.objects.create_user(user_id='student_user', password='password123')
        self.student.user = student_user
        self.student.save()

        # Log in as student
        self.client.force_login(student_user)
        res = self.client.get(reverse('students:my_library_books'))
        self.assertEqual(res.status_code, 200)


class OperationsTests(AcademicAndOperationsBaseTestCase):
    def test_transport_management(self):
        # Vehicle and route
        vehicle = Vehicle.objects.create(
            vehicle_number='DHK-1234',
            driver_name='Driver Khan',
            driver_phone='01700112233',
            capacity=30
        )
        route = TransportRoute.objects.create(
            route_name='Route North',
            vehicle=vehicle,
            start_point='Station',
            end_point='Campus',
            monthly_fare=600.00
        )

        res = self.client.get(reverse('students:transport_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Route North')

        # Allocate transport
        alloc_res = self.client.post(reverse('students:transport_list'), {
            'student': self.student.id,
            'route': route.id,
            'pickup_point': 'Station',
        })
        self.assertEqual(alloc_res.status_code, 302)
        self.assertTrue(StudentTransport.objects.filter(student=self.student).exists())

    def test_hostel_management(self):
        hostel = Hostel.objects.create(
            name='Central Boys Hostel',
            hostel_type='BOYS',
            warden_name='Dr. Warden',
            warden_phone='01811223344',
            address='West Campus'
        )
        room = HostelRoom.objects.create(
            hostel=hostel,
            room_number='101',
            capacity=4,
            cost_per_bed=1200.00
        )

        res = self.client.get(reverse('students:hostel_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Central Boys Hostel')

        # Allocate bed
        alloc_res = self.client.post(reverse('students:hostel_list'), {
            'student': self.student.id,
            'room': room.id,
            'bed_number': 'Bed 1'
        })
        self.assertEqual(alloc_res.status_code, 302)
        self.assertTrue(BedAllocation.objects.filter(student=self.student).exists())
        room.refresh_from_db()
        self.assertEqual(room.occupied_beds, 1)

    def test_leave_management(self):
        leave_type = LeaveType.objects.create(name='Casual Leave', days_allowed=15)

        # Apply for leave
        today = datetime.date.today()
        apply_res = self.client.post(reverse('students:leave_apply'), {
            'leave_type': leave_type.id,
            'start_date': today,
            'end_date': today + datetime.timedelta(days=2),
            'reason': 'Family commitment'
        })
        self.assertEqual(apply_res.status_code, 302)

        app = LeaveApplication.objects.get(applicant=self.staff_user)
        self.assertEqual(app.status, 'PENDING')

        # Approve leave
        approve_res = self.client.post(reverse('students:leave_manage'), {
            'application_id': app.id,
            'action': 'APPROVED',
            'admin_remarks': 'Approved'
        })
        self.assertEqual(approve_res.status_code, 302)
        app.refresh_from_db()
        self.assertEqual(app.status, 'APPROVED')


class AdmitCardTests(AcademicAndOperationsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.exam_year = ExamYear.objects.create(exam_year='2026', date=datetime.date(2026, 12, 1))
        self.exam = Exam.objects.create(name='Final Exam', exam_yea=self.exam_year)
        self.admit_card = ExamAdmitCard.objects.create(
            student=self.student,
            exam=self.exam,
            exam_year=self.exam_year,
            roll_number='EX-09A01',
            room_number='Room 201',
            seat_bench='Bench 1'
        )

    def test_admit_card_list_and_print(self):
        list_res = self.client.get(reverse('students:admit_cards'))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, 'EX-09A01')

        print_res = self.client.get(reverse('students:admit_card_print', args=[self.admit_card.id]))
        self.assertEqual(print_res.status_code, 200)
        self.assertContains(print_res, 'EXAMINATION ADMIT CARD')
        self.assertContains(print_res, 'Room 201')


class ParentPortalTests(AcademicAndOperationsBaseTestCase):
    def test_parent_portal_get(self):
        c = Client()
        res = c.get(reverse('parents_portal'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'অভিভাবক কর্নার')

    def test_parent_portal_post_valid_student(self):
        c = Client()
        post_data = {
            'roll': self.student.unique_roll,
            'phone': self.student.gurdian_mobile_number
        }
        res = c.post(reverse('parents_portal'), post_data)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.student.name)
        self.assertContains(res, 'Attendance')

    def test_parent_portal_post_invalid_student(self):
        c = Client()
        post_data = {
            'roll': 'INVALID_ROLL',
            'phone': '01999999999'
        }
        res = c.post(reverse('parents_portal'), post_data)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'No active student found')


class OnlineAdmissionEnrollTests(AcademicAndOperationsBaseTestCase):
    def test_enroll_online_applicant(self):
        # Ensure student group exists
        Group.objects.get_or_create(name='Student')

        applicant = OnlineAdmission.objects.create(
            student_name_en='Applicant John',
            student_name_bn='জন',
            student_father_name_en='Father John',
            student_father_name_bn='বাবা জন',
            student_mother_name_en='Mother John',
            student_mother_name_bn='মা জন',
            student_number='01700998877',
            gurdian_number='01800998877',
            gender_choise='Male',
            date_of_birth=datetime.date(2010, 5, 1),
            admission_fee=2500,
            present_address='Mirpur Dhaka',
            permanent_address='Mirpur Dhaka',
        )

        res = self.client.post(reverse('dashboard_management:online_admission_enroll', args=[applicant.id]), {
            'class_id': self.class_name.id,
            'section_id': self.section.id,
            'roll_number': '09A99',
            'session': '2025-2026'
        })
        self.assertEqual(res.status_code, 302)

        # Check student created
        self.assertTrue(StudentsInfo.objects.filter(unique_roll='09A99').exists())
        student = StudentsInfo.objects.get(unique_roll='09A99')
        self.assertEqual(student.name, 'Applicant John')
        self.assertIsNotNone(student.user)
        self.assertTrue(student.user.groups.filter(name='Student').exists())


class StudentDirectoryAndDetailTests(AcademicAndOperationsBaseTestCase):
    def test_student_list_view(self):
        res = self.client.get(reverse('students:students_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Student Directory')
        self.assertContains(res, self.student.name)

    def test_student_admin_detail_view(self):
        res = self.client.get(reverse('students:student_admin_detail', args=[self.student.id]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.student.name)
        self.assertContains(res, self.student.unique_roll)
        self.assertContains(res, 'Personal & Guardian Details')

    def test_student_create_form_get(self):
        res = self.client.get(reverse('students:students_create'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Register New Student')

