from django.test import TestCase
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models.loading import get_models
import json
from dynamic.models import *


class BasicTestCase(TestCase):
		
	def test_create_models(self):
		call_command('create_models', './test_models.xml')
		# check that 
		self.failUnlessEqual(User.objects.count(), 0)
		self.failUnlessEqual(Room.objects.count(), 0)
		
	def test_index(self):
		response = self.client.get(reverse('home'))
		self.failUnlessEqual(response.status_code, 200) 
		for i in get_models():
			if i._meta.app_label == 'dynamic':
				self.assertContains(response, i._meta.object_name)
		
	def test_create(self):
		# Fail when Method GET
		response = self.client.get(reverse('create-object'))
		self.failUnlessEqual(response.status_code, 405)
		
		# Error 404 when no param 'model_name'
		response = self.client.post(reverse('create-object'))
		self.failUnlessEqual(response.status_code, 404)
		
		# Error 404 when model_name with wrong model name
		response = self.client.post(reverse('create-object'), {'model_name': 'SomeModel'})
		self.failUnlessEqual(response.status_code, 404)
		
		# Send right params
		response = self.client.post(reverse('create-object'), {
			'model_name': 'User',
			'name': 'test name',
			'date_joined': '2014-01-01',
			'paycheck': 3
		})
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.content, json.dumps({"result": 1}))
		# Create new object after correct request
		self.failUnlessEqual(User.objects.count(), 1)
		
		# Send right params when not set object's field values
		response = self.client.post(reverse('create-object'), {'model_name': 'User'})
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.content, json.dumps({
			"errors": {
				"paycheck": ["This field is required."], 
				"name": ["This field is required."], 
				"date_joined": ["This field is required."]
			}, 
			"result": 0}))	  	
		
	def test_edit(self):
		# Fail when Method GET
		response = self.client.get(reverse('edit-object'))
		self.failUnlessEqual(response.status_code, 405)
		
		# Error 404 when no param 'model_name'
		response = self.client.post(reverse('edit-object'))
		self.failUnlessEqual(response.status_code, 404)
		
		# Error 404 when model_name with wrong model name
		response = self.client.post(reverse('edit-object'), {'model_name': 'SomeModel'})
		self.failUnlessEqual(response.status_code, 404)
		
		u = User(name='1', paycheck=2, date_joined = '2014-01-01')
		u.save()
		# Send right params with changing paycheck += 1
		response = self.client.post(reverse('edit-object'), {
			'model_name': 'User',
			'id': u.id,
			'name': u.name,
			'date_joined': u.date_joined,
			'paycheck': u.paycheck + 1 
		})
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.content, json.dumps({"result": 1}))	
		# Check that paycheck changed
		self.failUnlessEqual(User.objects.all()[0].paycheck, u.paycheck + 1)
	
		# Send right params when not set object's field values
		response = self.client.post(reverse('create-object'), {'model_name': 'User'})
		self.failUnlessEqual(response.status_code, 200)
		self.failUnlessEqual(response.content, json.dumps({
			"errors": {
				"paycheck": ["This field is required."], 
				"name": ["This field is required."], 
				"date_joined": ["This field is required."]
			}, 
			"result": 0}))
			
	
	def test_get_objects(self):
		# Send wrong model name
		response = self.client.get(reverse('get-objects', args=('SomeModel',)))
		self.failUnlessEqual(response.status_code, 404)
		
		# Send right model name
		response = self.client.get(reverse('get-objects', args=('User',)))
		self.failUnlessEqual(response.status_code, 200)    	
		self.failUnlessEqual(response.content, json.dumps({
			"name": "User",
			"objects": [],
			"fields":[
			     {"column": "id", "type": "AutoField", "name": "ID"},
			     {"column": "name", "type": "CharField", "name": "Name"},
			     {"column": "paycheck", "type": "IntegerField", "name": "Salary"},
			     {"column": "date_joined", "type": "DateField", "name": "Date of coming to work"}
			]
		}))

