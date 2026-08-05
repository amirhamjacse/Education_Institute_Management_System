# Missing / Incomplete Features

Audit of gaps found in the current codebase (as of 2026-08-05).

## Recently added

- **Attendance tracking** (2026-08-05) — implemented for both students and teachers:
  - Student side: `students.Attendance` model, class/section/date-based marking flow (`students:attendance_query` → `students:attendance_mark`) with editable re-entry per day, and a filterable `students:attendance_report` view. Linked from the Results Dashboard.
  - Teacher side: `institute_dashaboard.TeacherAttendance` model, date-based marking at `dashboard_management:teacher_attendance_mark` plus `dashboard_management:teacher_attendance_report`. Linked from the Portal Manager Dashboard.
  - Both use Django's auto-generated model permissions (`add_attendance` / `view_attendance`, staff-only for teacher attendance) and are registered in the admin.

## Core functionality gaps

- **Recurring fee / invoice management** — only a one-off `admission_fee` field on `OnlineAdmission` (`institute_dashaboard/models.py:138`). No tuition fee, dues, invoices, or payment history per student.
- **Real class routine / timetable** — `StudentsRoutine` (`students/views/students_dashboard.py:46`) just lists all students; there's no actual period/subject/time-slot model behind it.
- **Library management** — no book/borrowing models.
- **Transport management** — no vehicle/route models.
- **Hostel management** — none.
- **HR / payroll** — no salary, payslip, or leave management for teachers/staff.
- **Admit card generation** — student ID cards exist (`dashboard_management/views/id_card.py`) but there's no exam admit card.
- **SMS / email notifications** — no `EMAIL_BACKEND` configured in settings, and no SMS gateway despite Bangladesh-format phone validators used throughout the models.

## Login / portal gaps

- **Teachers, other staff, and `StudentsInfo` aren't linked to the `User` model** — no `OneToOneField` to `Core.User`, so teachers and students can't self-login and see their own dashboard. Only staff/admin accounts with explicit permissions can use the dashboards today.
- **No parent portal or parent role** at all.

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

1. Link `StudentsInfo` / `Teachers_Information` to `Core.User` so students and teachers can self-login.
2. Build recurring fee/invoice management, reusing the existing SSLCommerz integration.
3. Reconcile the duplicate models between `institute_dashaboard` and `students`.
4. Fill in real test coverage for the untested apps (including the new attendance views).
5. Harden production settings (env-based `SECRET_KEY`/`DEBUG`, security headers, email backend).
