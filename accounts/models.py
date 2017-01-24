from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, first_name, last_name, is_admin, **extra_fields):
		if not email:
			raise ValueError ('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, first_name=first_name, last_name=last_name, is_admin=is_admin)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, first_name, last_name, is_admin, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, first_name, last_name, False, **extra_fields)

	def create_superuser(self, email, password, first_name, last_name, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_user(email, password, first_name, last_name, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('email address', unique=True)
	first_name = models.CharField('first name', max_length=50, blank=False)
	last_name = models.CharField('last name', max_length=50, blank=False)
	company_name = models.CharField('company', max_length=200, blank=True)
	date_joined = models.DateTimeField('date joined', auto_now_add=True, auto_now=False)
	is_planner = models.BooleanField('is planner', default=False)
	is_active = models.BooleanField('active', default=True)
	is_admin = models.BooleanField('admin', default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])

	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	#Setting individual permissions for Django admin
	def has_perm(self, can_edit, obj=None):
		if self.is_admin:
			return True
	def has_perm(self, can_view, obj=None):
		if self.is_admin:
			return True

	def has_module_perms(self, accounts):
		if self.is_admin:
			return True
	def has_module_perms(self, tablesetter):
		if self.is_admin:
			return True

	def __str__(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name

