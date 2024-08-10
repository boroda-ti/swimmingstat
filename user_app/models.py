from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, initial_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, first_name=first_name, last_name=last_name, initial_name=initial_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_coach(self, email, first_name, last_name, initial_name, password=None, **extra_fields):
        user = self.create_user(email, first_name, last_name, initial_name, password, **extra_fields)
        user.is_coach = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, initial_name, password=None, **extra_fields):
        user = self.create_user(email, first_name, last_name, initial_name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    initial_name = models.CharField(max_length=30, default='-')
    date_of_birth = models.DateField(default=None, null=True, blank=True)

    school = models.ForeignKey('stats_app.School', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'initial_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.{self.initial_name[0]}. - {self.email}'