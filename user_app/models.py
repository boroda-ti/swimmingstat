from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Base user type

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AbstractUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth']

    class Meta:
        abstract = True


# Custom user types

RANK_CHOICES = [
        ('3Y', '3 юнацький'),
        ('2Y', '2 юнацький'),
        ('1Y', '1 юнацький'),
        ('3A', '3 дорослий'),
        ('2A', '2 дорослий'),
        ('1A', '1 дорослий'),
        ('CMS', 'КМС'),
        ('MS', 'МС'),
        ('MSMK', 'МСМК'),
    ]

class Athlete(AbstractUser):

    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True, blank=True)
    #results = 
    coach = models.ForeignKey('Coach', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.OneToOneField('School', on_delete=models.SET_NULL, null=True, blank=True)

class Coach(AbstractUser):

    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True, blank=True)
    school = models.OneToOneField('School', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Manager(AbstractUser):
    pass


# Additional shcool class
class School(models.Model):

    name = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name