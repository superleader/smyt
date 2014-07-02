from django.db.models.loading import get_models

import os
import xmltodict


class ModelGenerator:

	def __init__(self, file):
		self.file = file
	
	def run(self):
		try:
			doc = xmltodict.parse(self.file.read())	
		except:
			return False
		result, admin, form = self.parseXML(doc)
		mfile = open('dynamic/models.py', 'w')
		mfile.write(result)
		mfile.close()
		
		os.system('./manage.py schemamigration dynamic --auto')
		os.system('./manage.py migrate dynamic')
		
		mfile = open('dynamic/admin.py', 'w')
		mfile.write(admin)
		mfile.close()
		
		mfile = open('dynamic/forms.py', 'w')
		mfile.write(form)
		mfile.close()
		return True
		
		
	def parseXML(self, doc):		
		result = "# -*- coding: utf-8 -*-\nfrom django.db import models\nfrom django.utils.translation import ugettext as _\n\n\n"
		form = 'from django.forms import ModelForm\nfrom dynamic.models import *\n\n'		
		admin = "from django.contrib import admin\nfrom dynamic.models import *\n\n"
		for k, v in doc['models'].items():
			model = k.title()[:-1]
			#models.append(model)
			admin += "admin.site.register(globals().get('%s'))\n" % model
			form += 'class %sForm(ModelForm):\n\tclass Meta:\n\t\tmodel = %s\n\n' \
				% (model, model)
			result += "class %s(models.Model):\n\tdb_table = '%s'\n\n" \
				% (model, k)
			for i, j in v.items():
				if type(j) == list:
					for ki in j:
						name = ''
						_type = ''
						title = ''
						for vi, vj in ki.items():
							if vi == '@id':
								name = '%s' % vj
							elif vi == '@type':
								if vj == 'char':
									_type = 'Char'
								elif vj == 'int':
									_type = 'Integer'
								elif vj == 'date':
									_type = 'Date'
							elif vi == '@title':
								title = vj
						if name and title and _type:
							result += "\t%s = models.%sField(_('%s')%s)\n" % \
								(name, _type, title, ', max_length=255' \
										if _type == 'Char' else '')
					result += '\n\n'
		result += '\n'
		form += '\n'	
		return result, admin, form
	