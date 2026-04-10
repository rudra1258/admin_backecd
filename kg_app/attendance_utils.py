# attendance_utils.py

from django.utils import timezone
from datetime import time, date, timedelta
from .models import Attendance, leave_request

PRESENT_CUTOFF = time(10, 30)   # login before 10:30 AM → Present
ABSENT_CUTOFF  = time(14, 0)    # no login by 2:00 PM  → Absent

def mark_attendance_on_login(user, admin_id, login_datetime):
    """
    Called from create_gs_login view.
    Marks attendance for today based on login time.
    """
    today = login_datetime.date()
    login_time_only = login_datetime.time()

    # Check if user has an approved leave for today
    on_leave = leave_request.objects.filter(
        user_id=user,
        from_date__lte=today,
        to_date__gte=today,
        leave_status='Approved'
    ).exists()

    if on_leave:
        _upsert_attendance(user, admin_id, today, 'Leave', login_datetime)
        return 'Leave'

    # Present if logged in before or at 10:30 AM
    if login_time_only <= PRESENT_CUTOFF:
        _upsert_attendance(user, admin_id, today, 'Present', login_datetime)
        return 'Present'

    # Late but still logged in — mark Present (you can change to 'Late' if needed)
    _upsert_attendance(user, admin_id, today, 'Present', login_datetime)
    return 'Present'


def _upsert_attendance(user, admin_id, day, status, login_dt=None):
    """Create or update the attendance record for a given day."""
    obj, created = Attendance.objects.update_or_create(
        user_id=user,
        date=day,
        defaults={
            'admin_id':   admin_id,
            'status':     status,
            'login_time': login_dt,
            'marked_by':  'auto',
        }
    )
    return obj


def auto_mark_absent():
    """
    Run this via a Celery beat task or cron at 2:00 PM every day.
    Marks Absent for any user who hasn't logged in yet today.
    """
    from .models import CreateUser   # import here to avoid circular import
    today = date.today()
    cutoff_dt = timezone.now().replace(hour=14, minute=0, second=0, microsecond=0)

    if timezone.now() < cutoff_dt:
        return  # don't run before 2 PM

    all_users = CreateUser.objects.filter(is_active=True)
    for user in all_users:
        on_leave = leave_request.objects.filter(
            user_id=user,
            from_date__lte=today,
            to_date__gte=today,
            leave_status='Approved'
        ).exists()

        Attendance.objects.get_or_create(
            user_id=user,
            date=today,
            defaults={
                'admin_id':  getattr(user, 'admin_id', ''),
                'status':    'Leave' if on_leave else 'Absent',
                'marked_by': 'auto',
            }
        )