from django.shortcuts import redirect
from django.contrib import messages

def superadmin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check 1: Are they logged in?
        if 'admin_username' not in request.session:
            return redirect('admin_login')
        
        # Check 2: Are they actually a Super Admin?
        # We check the role we saved in the session during login
        if request.session.get('admin_role') != 'superadmin':
            messages.error(request, "Access Denied: Super Admin permissions required.")
            return redirect('admin_home') # Send them back to their own area
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view