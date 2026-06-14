from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('GA', 'Главный администратор'),
        ('SENIOR', 'Старший администратор'),
        ('ADMIN', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ADMIN')

    def can_accept_governor(self):
        return self.role in ['GA', 'SENIOR']
    
    def can_manage_admins(self):
        return self.role == 'GA'

class Application(models.Model):
    DEPARTMENT_CHOICES = [
        ('GOVERNOR', 'Администрация губернатора'),
        ('JUSTICE', 'Министерство Юстиции'),
        ('BAR', 'Адвокатура'),
    ]
    static_field = models.CharField(max_length=255) 
    full_name = models.CharField(max_length=255) 
    age = models.PositiveIntegerField() 
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

class LogEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)