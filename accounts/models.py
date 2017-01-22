from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, first_name, last_name, **extra_fields):
		if not email:
			raise ValueError ('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, first_name=first_name, last_name=last_name)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, first_name, last_name, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, first_name, last_name)

	def _create_planner_user(self, email, password, first_name, last_name, company_name, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		planner_user = self.model(email=email, first_name=first_name,last_name=last_name,
			is_planner=True, company_name=company_name)
		planner_user.set_password(password)
		planner_user.save(using=self._db)
		return planner_user

	def create_planner_user(self, email, password, first_name, last_name, company_name, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_planner_user(email, password, first_name, 
			last_name, company_name, **extra_fields)

	def _create_superuser(self, email, password, first_name, last_name, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		superuser = self.model(email=email, first_name=first_name, last_name=last_name, is_staff=True)
		superuser.set_password(password)
		superuser.save(using=self._db)
		return superuser

	def create_superuser(self, email, password, first_name, last_name, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_superuser(email, password, first_name, last_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=50, blank=False)
	last_name = models.CharField(_('last name'), max_length=50, blank=False)
	company_name = models.CharField(_('company'), max_length=100, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_planner = models.BooleanField(_('planner'), default=False)
	is_staff = models.BooleanField(_('staff'), default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])

	def __str__(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name

