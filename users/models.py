from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for handling multiple user types.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email, password, and user type.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        # if not user_type:
        #     raise ValueError(_('The UserType field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'Admin')
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model supporting multiple user types.
    """
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Seller', 'Seller'),
        ('Client', 'Client'),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.email} ({self.get_user_type_display()})'

    def get_full_name(self):
        """
        Return the full name of the user.
        """
        return self.name

    def get_short_name(self):
        """
        Return the short name of the user.
        """
        return self.name.split(" ")[0]

    def soft_delete(self):
        """
        Soft delete the user by setting the is_active field to False.
        """
        self.is_active = False
        self.save()

    def restore(self):
        """
        Restore a soft-deleted user by setting the is_active field to True.
        """
        self.is_active = True
        self.save()

    def is_admin(self):
        """
        Check if the user is an Admin.
        """
        return self.user_type == 'Admin'

    def is_seller(self):
        """
        Check if the user is a Seller.
        """
        return self.user_type == 'Seller'

    def is_client(self):
        """
        Check if the user is a Client.
        """
        return self.user_type == 'Client'


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
