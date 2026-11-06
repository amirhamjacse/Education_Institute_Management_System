from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from .commonfields import CommonFields
from .students_info import StudentsInfo


# ==============================================================================
# TRANSPORT MANAGEMENT
# ==============================================================================

class Vehicle(CommonFields):
    """Institutional transportation vehicle"""
    vehicle_number = models.CharField(_('Vehicle Number / Plate'), max_length=50, unique=True)
    vehicle_model = models.CharField(_('Vehicle Model'), max_length=100, blank=True, default='')
    driver_name = models.CharField(_('Driver Name'), max_length=150)
    driver_phone = models.CharField(_('Driver Phone Number'), max_length=20)
    capacity = models.PositiveIntegerField(_('Seating Capacity'), default=30)

    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_model}) - Driver: {self.driver_name}"


class TransportRoute(CommonFields):
    """Transport route and fee structure"""
    route_name = models.CharField(_('Route Name'), max_length=150)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routes'
    )
    start_point = models.CharField(_('Start Location'), max_length=150)
    end_point = models.CharField(_('End Location'), max_length=150)
    monthly_fare = models.DecimalField(_('Monthly Fare (BDT)'), max_digits=8, decimal_places=2, default=500.00)
    stops_description = models.TextField(_('Stops & Timing Details'), blank=True, default='')

    def __str__(self):
        return f"{self.route_name} ({self.start_point} to {self.end_point})"


class StudentTransport(CommonFields):
    """Student transport allocation"""
    student = models.OneToOneField(
        StudentsInfo,
        on_delete=models.CASCADE,
        related_name='transport_record'
    )
    route = models.ForeignKey(
        TransportRoute,
        on_delete=models.CASCADE,
        related_name='student_allocations'
    )
    pickup_point = models.CharField(_('Pickup / Dropoff Point'), max_length=150)

    def __str__(self):
        return f"{self.student.name} - {self.route.route_name}"


# ==============================================================================
# HOSTEL / DORMITORY MANAGEMENT
# ==============================================================================

class Hostel(CommonFields):
    """Hostel building definition"""
    HOSTEL_TYPES = [
        ('BOYS', 'Boys Hostel'),
        ('GIRLS', 'Girls Hostel'),
        ('STAFF', 'Staff Quarters'),
    ]

    name = models.CharField(_('Hostel Name'), max_length=150, unique=True)
    hostel_type = models.CharField(_('Hostel Type'), max_length=20, choices=HOSTEL_TYPES)
    warden_name = models.CharField(_('Warden Name'), max_length=150)
    warden_phone = models.CharField(_('Warden Phone'), max_length=20)
    address = models.TextField(_('Hostel Location / Address'))

    def __str__(self):
        return f"{self.name} ({self.get_hostel_type_display()})"


class HostelRoom(CommonFields):
    """Room inside a hostel"""
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    room_number = models.CharField(_('Room Number'), max_length=50)
    capacity = models.PositiveIntegerField(_('Bed Capacity'), default=4)
    occupied_beds = models.PositiveIntegerField(_('Occupied Beds'), default=0)
    cost_per_bed = models.DecimalField(_('Monthly Cost Per Bed (BDT)'), max_digits=8, decimal_places=2, default=1500.00)

    class Meta:
        unique_together = ('hostel', 'room_number')

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

    @property
    def is_full(self):
        return self.occupied_beds >= self.capacity


class BedAllocation(CommonFields):
    """Student bed allocation in a hostel room"""
    room = models.ForeignKey(
        HostelRoom,
        on_delete=models.CASCADE,
        related_name='allocations'
    )
    student = models.OneToOneField(
        StudentsInfo,
        on_delete=models.CASCADE,
        related_name='hostel_allocation'
    )
    bed_number = models.CharField(_('Bed Number / Identifier'), max_length=20, default='Bed 1')
    allocated_date = models.DateField(_('Allocation Date'), default=timezone.now)

    def __str__(self):
        return f"{self.student.name} -> {self.room} ({self.bed_number})"


# ==============================================================================
# LEAVE MANAGEMENT (HR)
# ==============================================================================

class LeaveType(CommonFields):
    """Types of leaves (Casual, Sick, Maternity, etc.)"""
    name = models.CharField(_('Leave Type Name'), max_length=100, unique=True)
    days_allowed = models.PositiveIntegerField(_('Annual Allowance (Days)'), default=15)

    def __str__(self):
        return f"{self.name} ({self.days_allowed} days/year)"


class LeaveApplication(CommonFields):
    """Staff/Teacher leave requests and approval lifecycle"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_applications'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    reason = models.TextField(_('Reason for Leave'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    admin_remarks = models.TextField(_('Admin Remarks'), blank=True, default='')

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f"Leave: {self.applicant.get_full_name() or self.applicant.user_id} ({self.start_date} to {self.end_date}) [{self.status}]"
