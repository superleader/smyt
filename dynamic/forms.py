from django.forms import ModelForm
from dynamic.models import *

class UserForm(ModelForm):
	class Meta:
		model = User

class RoomForm(ModelForm):
	class Meta:
		model = Room


