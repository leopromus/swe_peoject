from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields['role'] = role
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, role='Admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, role, **extra_fields)


# User model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Judge', 'Judge'),
        ('Lawyer', 'Lawyer'),
        ('Registrar', 'Registrar'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Admin'
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.role}"

# Court Case model
class CourtCase(models.Model):
    CIN = models.AutoField(primary_key=True)
    defendant_name = models.CharField(max_length=255)
    defendant_address = models.TextField()
    crime_type = models.CharField(max_length=100)
    crime_date = models.DateField()
    crime_location = models.CharField(max_length=255)
    arresting_officer = models.CharField(max_length=255)
    arrest_date = models.DateField()
    hearing_date = models.DateField(null=True, blank=True)
    adjournment_reason = models.TextField(blank=True)
    hearing_summary = models.TextField(blank=True)
    judgment_summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Closed', 'Closed')])
    judge = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='judge_cases', null=True)
    lawyer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='lawyer_cases', null=True)
    public_prosecutor = models.CharField(max_length=255)
    starting_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

# Payment model
class Payment(models.Model):
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE)
    court_case = models.ForeignKey(CourtCase, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
