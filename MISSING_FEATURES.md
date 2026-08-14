# Missing / Incomplete Features

Audit of gaps found in the current codebase (as of 2026-08-05).

## Recently added

- **Attendance tracking** (2026-08-05) — implemented for both students and teachers:
  - Student side: `students.Attendance` model, class/section/date-based marking flow (`students:attendance_query` → `students:attendance_mark`) with editable re-entry per day, and a filterable `students:attendance_report` view. Linked from the Results Dashboard.
  - Teacher side: `institute_dashaboard.TeacherAttendance` model, date-based marking at `dashboard_management:teacher_attendance_mark` plus `dashboard_management:teacher_attendance_report`. Linked from the Portal Manager Dashboard.
  - Both use Django's auto-generated model permissions (`add_attendance` / `view_attendance`, staff-only for teacher attendance) and are registered in the admin.

- **Fee & invoice management** (2026-08-14) — new `fees` app: `FeeHead`/`FeeStructure` lookup tables (per class + session + frequency), `Invoice`/`Payment` models with staff-recorded payments (cash/bank/mobile banking — no online checkout), bulk invoice generation per class/section/period plus ad-hoc single-student invoices, a filterable/paginated invoice list, an invoice detail view with payment history, payment recording (`select_for_update`-guarded against concurrent posting), payment voiding, a printable receipt, an overdue-invoices view, and a collection report (total invoiced/collected/due, by class). Linked from the Portal Manager Dashboard. Uses Django's auto-generated model permissions (`fees.add_invoice`, `fees.add_payment`, `fees.view_invoice`, etc.) — assignable to regular staff, unlike `dashboard_management`'s permission gap below.
  - **Deferred**: online payment checkout (the existing SSLCommerz integration in `institute_dashaboard/views.py` is dead code — its callback URLs have no matching route and `Transaction` is never written to; wiring it up is a separate task), SMS/email due-date reminders (no notification layer exists), scheduled/automatic recurring invoice generation (no Celery — use the manual "generate for period" bulk action instead), expense tracking (a separate finance concern from fee collection).

- **Student/teacher self-login** (2026-08-14) — `StudentsInfo`, `Teachers_Information`, and `Other_Employee_Information` now have a real `user` `OneToOneField` to `Core.User` (backfilled for existing rows via the old `unique_roll == user_id` convention). Account creation was rewritten across the board:
  - Passwords are now randomly generated (`Core.utils.generate_temp_password`) instead of the student's own phone number, shown once via a success message for the admin to share securely — the old behavior let anyone who knew a student's phone number log in as them.
  - Teacher/staff creation (`AddTeacherView`/`AddStuff`) now actually creates a login (previously created none at all) and is auth/permission-gated (previously reachable with no login at all).
  - Accounts are added to real, named `Group`s (`Student`, `Teacher`, `Staff`) instead of a hardcoded `Group.objects.get(id=1)` that doesn't exist in a fresh install.
  - Fixed the pre-existing role-based post-login hub (`students:dashobard_app` / `dashobard.html`) and its `ResultsDashboard`/`StudentsInfoDashboard`/`StudentsDashboard` targets, which were built to key off these groups but never worked: `ResultsDashboard`/`StudentsInfoDashboard` required `students.view_students`, a permission that doesn't exist for any real model (only a superuser could ever pass it) — fixed to real permissions / group checks. `SDashboard`/`StudentsDashboard` never populated the `students` context variable their own templates already expected, so "My Profile", "My Subjects", and "Register for new class" links never rendered — now populated from `request.user.student_profile`.
  - `students:students_specific_result` ("My Result") now auto-scopes to the logged-in student's own roll number when they have a linked profile, instead of trusting an arbitrary POSTed roll number.
  - New self-service `fees:my_invoices` view lets a logged-in student see and print their own invoices/receipts, gated by ownership (`student_profile`) rather than the staff-wide `fees.view_invoice` permission.
  - Retroactive login creation for pre-existing teacher/staff/student rows via a "Create login accounts for selected" admin action.
  - **Residual gaps, left alone deliberately**: `StudentsSubjects`/`StudentsClassRegister` ("My Subjects"/"Register for new class") still require `students.add_resultinfo`, which the `Student` group isn't granted — letting students self-register into any class is a business-rule decision, not made here. No dedicated dashboard card for the `Staff` role. Credentials are still shared manually (no `EMAIL_BACKEND`/SMS). Django's password reset/change flow is still unwired (missing `templates/registration/password_reset_*.html`).

## Core functionality gaps

- **Real class routine / timetable** — `StudentsRoutine` (`students/views/students_dashboard.py:46`) just lists all students; there's no actual period/subject/time-slot model behind it.
- **Library management** — no book/borrowing models.
- **Transport management** — no vehicle/route models.
- **Hostel management** — none.
- **HR / payroll** — no salary, payslip, or leave management for teachers/staff.
- **Admit card generation** — student ID cards exist (`dashboard_management/views/id_card.py`) but there's no exam admit card.
- **SMS / email notifications** — no `EMAIL_BACKEND` configured in settings, and no SMS gateway despite Bangladesh-format phone validators used throughout the models.

## Login / portal gaps

- **No parent portal or parent role** at all.
- Django's built-in password reset/change flow is wired via `django.contrib.auth.urls` but non-functional — the required templates (`templates/registration/password_reset_*.html`, `password_change_*.html`) don't exist.

## Architectural debt

- **Duplicate, unreconciled models** — `institute_dashaboard.Students_Information` / `Teachers_Information` / `Result` overlap with `students.StudentsInfo` / `ResultInfo`, suggesting the public-site admission flow and the academic-records app were never fully merged.
- **`django-import-export` is only wired for the `Core.User` admin**, not for bulk student/result import, which would be the more useful case.

## Quality / production readiness

- **Test coverage** — only the `Core` app has real tests. `students`, `dashboard_management`, `institute_dashaboard`, and `websitesetting` all still have the untouched Django stub (`# Create your tests here.`).
- **`DEBUG = True` and a hardcoded `SECRET_KEY`** are committed in settings (`CONFIG/settings.py:29`, `CONFIG/local_setting.py`) — not environment-based.
- No `SECURE_*` / HSTS / CSRF-cookie hardening, no `CACHES` configuration.
- Leftover debug `print()` statements in view code (e.g. `students/views/students_dashboard.py:35`, `students/views/create_students.py`).
- No REST API layer (no Django REST Framework) if a mobile app or external integration is ever planned.

## Suggested priority

1. Fix the dead SSLCommerz callback routing in `institute_dashaboard` so online payment (admission fee today, invoice payment tomorrow) actually works end to end.
2. Reconcile the duplicate models between `institute_dashaboard` and `students`.
3. Fill in real test coverage for the untested apps (including the new attendance, fee-management, and self-login views).
4. Harden production settings (env-based `SECRET_KEY`/`DEBUG`, security headers, email backend) — also needed before credentials can be delivered by email instead of shown once in the admin UI.
5. Wire up Django's password reset/change templates now that real per-user logins exist.
