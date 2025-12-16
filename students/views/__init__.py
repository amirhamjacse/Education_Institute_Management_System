from .create_students import StudentsCreateView, StudentsListView
from .dashboard import (
    SDashboard, StudentsInfoDashboard, ResultsDashboard, StudentsDashboard
)
from .result import (
    ResultsCreateView, ListOfResultsAddView, ListOfResultscCeateResultView,
    ShowResultView, SemesterResultView, SemesterResultViews
)
from .students_dashboard import (
    StudentsSubjects, StudentsRoutine, StudentsClassRegister,
    StudentsResultSpecific
)


__all__ = [
    StudentsCreateView, StudentsListView, SDashboard,
    ResultsCreateView, StudentsInfoDashboard, ListOfResultsAddView,
    ListOfResultscCeateResultView, ResultsDashboard, ShowResultView,
    SemesterResultView, SemesterResultViews, StudentsDashboard,
    StudentsSubjects, StudentsRoutine, StudentsClassRegister,
    StudentsResultSpecific
]
