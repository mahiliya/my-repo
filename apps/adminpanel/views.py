from django.shortcuts import render, redirect
from .models import Admin
from .forms import AdminLoginForm

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = Admin.objects.get(username=username)
            except Admin.DoesNotExist:
                return render(request, 'AdminLogin.html', {'form': form, 'error': 'Invalid username or password'})

            if admin.check_password(password):
                # Save login info in session
                request.session['admin_username'] = admin.username
                return redirect('admin_home')  # URL name for admin.html
            else:
                return render(request, 'AdminLogin.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AdminLoginForm()
    return render(request, 'AdminLogin.html', {'form': form})


def admin_home(request):
    if 'admin_username' not in request.session:
        return redirect('admin_login')
    return render(request, 'admin.html')
