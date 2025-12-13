from .models import *

def notification_context(request):
    """
    Context processor to make recent task updates available to all templates
    """
    # Get the session admin_id
    session_admin_id = request.session.get("admin_id")
    
    # Initialize empty values
    recent_updates = []
    notification_count = 0
    
    # Only fetch data if admin is logged in
    if session_admin_id:
        try:
            admin_id_pk = admin_user_model.objects.get(pk=session_admin_id)
            
            # Filter task updates by the logged-in admin
            recent_updates = task_update.objects.select_related(
                'admin_id', 'task_id'
            ).filter(admin_id=admin_id_pk).order_by('-updated_at')[:4]
            
            # Count only the updates for this admin
            notification_count = task_update.objects.filter(admin_id=admin_id_pk).count()
            
        except admin_user_model.DoesNotExist:
            # Admin not found, return empty data
            pass
    
    return {
        'recent_updates': recent_updates,
        'notification_count': notification_count,
    }