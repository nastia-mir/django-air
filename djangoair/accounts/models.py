from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class MyUserManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_airlines_staff', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **other_fields)

    def create_user(self, email=None, password=None, **other_fields):
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    is_airlines_staff = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MyUserManager()

    def __str__(self):
        return '{} {}, email: {}'.format(self.first_name, self.last_name, self.email)


class Passenger(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="passenger")
    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.user)


class Staff(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,  related_name="staff")

    roles = (
        ('gate_manager', 'Gate manager'),
        ('checkin_manager', 'Checkin manager'),
        ('supervisor', 'Supervisor')
    )
    role = models.CharField(max_length=50, choices=roles, blank=True)

    objects = models.Manager()

    def __str__(self):
        return '{} is airline staff, role: {}'.format(self.user, self.role)

