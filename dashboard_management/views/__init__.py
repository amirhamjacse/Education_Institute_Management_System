from .admission_dashboard import (
    OnlineAdmissionProcess
    )

from .portal_management import (
    PortalManagerDashboard, ADDNotice, DeleteNotice, AddNews,
    DeleteNews, GalleryView, AddTeacherView, AddStuff
)
from .assigned_classes import (
    AssignClassesToTeacher
)
__all__ = [
    OnlineAdmissionProcess,
    PortalManagerDashboard,
    AssignClassesToTeacher,
    ADDNotice,
    DeleteNotice,
    AddNews,
    DeleteNews,
    GalleryView,
    AddTeacherView,
    AddStuff
]