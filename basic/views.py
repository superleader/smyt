from annoying.decorators import render_to, ajax_request
from django.db.models.loading import get_models
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import Http404

from dynamic.forms import *
from dynamic.models import *
from basic.modelgenerator import ModelGenerator


@render_to('index.html')
def index(request):
	if request.FILES.get('xml'):
		generate_error = not(ModelGenerator(request.FILES['xml']).run())
	models = [ i._meta.object_name for i in get_models() \
	           if i._meta.app_label == 'dynamic']
	return locals()

	
@ajax_request
def get_objects(request, model):
	if not globals().get(model):
		raise Http404
	Model = globals()[model]
	objects = []
	for v in Model.objects.values():
		objects.append({})
		for i in v:
			objects[ len(objects) - 1 ][i] = str(v[i])
	return {
		'name': model,
		'objects': objects,
		'fields':[{
			'column': j.attname, 
			'type': j.__class__.__name__, 
			'name': j.verbose_name
			} for j in Model._meta.fields]
		}


@ajax_request
@require_POST
def create(request):
	if not request.POST.get('model_name') or not globals().get('%sForm' % request.POST['model_name']):
		raise Http404	
	
	form = globals()['%sForm' % request.POST['model_name'] ](request.POST)
	if form.is_valid():
		form.save()
		return {'result': 1}
	return {'result': 0, 'errors': form.errors }

	
@ajax_request
@require_POST
def edit(request):
	if not request.POST.get('model_name') or not globals().get(request.POST['model_name']):
		raise Http404
	
	object = get_object_or_404(globals()[ request.POST['model_name'] ], pk=request.POST['id'])
	form = globals()['%sForm' % request.POST['model_name'] ](request.POST, instance=object)
	if form.is_valid():
		form.save()
		return {'result': 1}
	return {'result': 0, 'errors': form.errors }
