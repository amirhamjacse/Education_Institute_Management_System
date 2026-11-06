from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from students.models import (
    Vehicle, TransportRoute, StudentTransport,
    Hostel, HostelRoom, BedAllocation,
    LeaveType, LeaveApplication, StudentsInfo
)
from institute_dashaboard.models import Web_Heading


class TransportManagementView(LoginRequiredMixin, View):
    """View and manage institutional routes and vehicle allocations"""
    template_name = 'operations/transport_list.html'

    def get(self, request, *args, **kwargs):
        routes = TransportRoute.objects.all().select_related('vehicle')
        vehicles = Vehicle.objects.all()
        students = StudentsInfo.objects.filter(is_active=True)
        allocations = StudentTransport.objects.all().select_related('student', 'route')

        # If logged in as student, find their route
        my_transport = None
        if hasattr(request.user, 'student_profile'):
            my_transport = StudentTransport.objects.filter(student=request.user.student_profile).first()

        webheading = Web_Heading.objects.last()
        return render(request, self.template_name, {
            'routes': routes,
            'vehicles': vehicles,
            'students_list': students,
            'allocations': allocations,
            'my_transport': my_transport,
            'webname': webheading,
        })

    def post(self, request, *args, **kwargs):
        """Allocate a student to a route (staff only)"""
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('students:transport_list')

        student_id = request.POST.get('student')
        route_id = request.POST.get('route')
        pickup = request.POST.get('pickup_point', 'Campus Gate')

        student = get_object_or_404(StudentsInfo, id=student_id)
        route = get_object_or_404(TransportRoute, id=route_id)

        StudentTransport.objects.update_or_create(
            student=student,
            defaults={'route': route, 'pickup_point': pickup}
        )
        messages.success(request, f'Allocated {student.name} to route {route.route_name}.')
        return redirect('students:transport_list')


class HostelManagementView(LoginRequiredMixin, View):
    """View and manage hostel facilities and student bed allocations"""
    template_name = 'operations/hostel_list.html'

    def get(self, request, *args, **kwargs):
        hostels = Hostel.objects.all().prefetch_related('rooms')
        rooms = HostelRoom.objects.all().select_related('hostel')
        students = StudentsInfo.objects.filter(is_active=True)
        allocations = BedAllocation.objects.all().select_related('student', 'room', 'room__hostel')

        my_hostel = None
        if hasattr(request.user, 'student_profile'):
            my_hostel = BedAllocation.objects.filter(student=request.user.student_profile).first()

        webheading = Web_Heading.objects.last()
        return render(request, self.template_name, {
            'hostels': hostels,
            'rooms': rooms,
            'students_list': students,
            'allocations': allocations,
            'my_hostel': my_hostel,
            'webname': webheading,
        })

    def post(self, request, *args, **kwargs):
        """Allocate a bed to a student (staff only)"""
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('students:hostel_list')

        student_id = request.POST.get('student')
        room_id = request.POST.get('room')
        bed_number = request.POST.get('bed_number', 'Bed 1')

        student = get_object_or_404(StudentsInfo, id=student_id)
        room = get_object_or_404(HostelRoom, id=room_id)

        if room.is_full:
            messages.error(request, f'Room {room.room_number} is already fully occupied.')
            return redirect('students:hostel_list')

        BedAllocation.objects.update_or_create(
            student=student,
            defaults={'room': room, 'bed_number': bed_number}
        )
        room.occupied_beds = room.allocations.count()
        room.save()

        messages.success(request, f'Allocated {student.name} to {room} ({bed_number}).')
        return redirect('students:hostel_list')


class LeaveApplicationView(LoginRequiredMixin, View):
    """Apply for leave and view application history for teachers & staff"""
    template_name = 'operations/leave_apply.html'

    def get(self, request, *args, **kwargs):
        leave_types = LeaveType.objects.all()
        my_leaves = LeaveApplication.objects.filter(applicant=request.user).order_by('-created_time')
        webheading = Web_Heading.objects.last()

        return render(request, self.template_name, {
            'leave_types': leave_types,
            'my_leaves': my_leaves,
            'webname': webheading,
        })

    def post(self, request, *args, **kwargs):
        leave_type_id = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        if not (leave_type_id and start_date and end_date and reason):
            messages.error(request, 'All fields are required.')
            return redirect('students:leave_apply')

        leave_type = get_object_or_404(LeaveType, id=leave_type_id)
        LeaveApplication.objects.create(
            applicant=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='PENDING',
        )
        messages.success(request, 'Your leave request has been submitted for approval.')
        return redirect('students:leave_apply')


class LeaveApprovalDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Manage and approve staff/teacher leave requests"""
    template_name = 'operations/leave_list.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', 'PENDING')
        leaves = LeaveApplication.objects.all().select_related('applicant', 'leave_type', 'approved_by')

        if status_filter != 'ALL':
            leaves = leaves.filter(status=status_filter)

        webheading = Web_Heading.objects.last()
        return render(request, self.template_name, {
            'leaves': leaves,
            'current_status': status_filter,
            'webname': webheading,
            'pending_count': LeaveApplication.objects.filter(status='PENDING').count(),
        })

    def post(self, request, pk=None, *args, **kwargs):
        action = request.POST.get('action')  # APPROVE or REJECT
        remarks = request.POST.get('admin_remarks', '')
        leave_id = pk or request.POST.get('application_id') or request.POST.get('leave_id')

        leave = get_object_or_404(LeaveApplication, pk=leave_id)
        if action in ['APPROVE', 'APPROVED']:
            leave.status = 'APPROVED'
        elif action in ['REJECT', 'REJECTED']:
            leave.status = 'REJECTED'

        leave.approved_by = request.user
        leave.admin_remarks = remarks
        leave.save()

        messages.success(request, f'Leave application {leave.id} marked as {leave.status}.')
        return redirect('students:leave_manage')
