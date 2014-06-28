# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class User(models.Model):
	db_table = 'users'

	name = models.CharField(_('Name'), max_length=255)
	paycheck = models.IntegerField(_('Salary'))
	date_joined = models.DateField(_('Date of coming to work'))


class Room(models.Model):
	db_table = 'rooms'

	department = models.CharField(_('Department'), max_length=255)
	spots = models.IntegerField(_('Capacity'))



