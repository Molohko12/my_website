from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import requests
from .models import Application, LogEntry, CustomUser
from .forms import ApplicationForm

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = 'Неверный логин или пароль'
    return render(request, 'admin_panel/login.html', {'error': error})

def auth_logout(request):
    logout(request)
    return redirect('/')

@login_required
@user_passes_test(lambda u: u.role in ['GA', 'SENIOR'])
def logs_view(request):
    log_entries = LogEntry.objects.all().order_by('-timestamp')
    return render(request, 'admin_panel/logs.html', {'log_entries': log_entries})

@login_required
def applications_view(request):
    applications = Application.objects.filter(status='pending')
    return render(request, 'admin_panel/applications.html', {'applications': applications})

@login_required
def accept_application(request, app_id):
    application = get_object_or_404(Application, pk=app_id)
    if application.department == 'GOVERNOR' and not request.user.can_accept_governor():
        return redirect('applications')
    application.status = 'accepted'
    application.processed_by = request.user
    application.save()
    LogEntry.objects.create(
        user=request.user,
        action=f"Принята заявка №{application.id} ({application.get_department_display()})"
    )
    return redirect('applications')

@login_required
@user_passes_test(user_is_ga)
def admins_view(request):
    users = CustomUser.objects.exclude(username=request.user.username)
    return render(request, 'admin_panel/admins.html', {'users': users})

@login_required
@user_passes_test(user_is_ga)
def change_role(request, user_id):
    if request.method == 'POST':
        new_role = request.POST.get('role')
        user_to_change = get_object_or_404(CustomUser, pk=user_id)
        user_to_change.role = new_role
        user_to_change.save()
        LogEntry.objects.create(
            user=request.user,
            action=f"Изменена роль пользователя {user_to_change.username} на {new_role}"
        )
    return redirect('admins')