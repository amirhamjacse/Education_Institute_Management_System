from .create_students import StudentsCreateView, StudentsListView, StudentsUpdateView, StudentsDeleteView
from .student_detail import StudentAdminDetailView
from .dashboard import (
    SDashboard, StudentsInfoDashboard, ResultsDashboard, StudentsDashboard
)
from .result import (
    ResultsCreateView, ListOfResultsAddView, ListOfResultscCeateResultView,
    ShowResultView, SemesterResultView, SemesterResultViews,
    ResultsAddedSuccessView
)
from .students_dashboard import (
    StudentsSubjects, StudentsRoutine, StudentsClassRegister,
    StudentsResultSpecific
)
from .attendance import (
    AttendanceQueryView, AttendanceMarkView, AttendanceReportView
)


__all__ = [
    StudentsCreateView, StudentsListView, StudentsUpdateView, StudentsDeleteView,
    StudentAdminDetailView, SDashboard,
    ResultsCreateView, StudentsInfoDashboard, ListOfResultsAddView,
    ListOfResultscCeateResultView, ResultsDashboard, ShowResultView,
    SemesterResultView, SemesterResultViews, StudentsDashboard,
    StudentsSubjects, StudentsRoutine, StudentsClassRegister,
    StudentsResultSpecific, ResultsAddedSuccessView,
    AttendanceQueryView, AttendanceMarkView, AttendanceReportView,
]
