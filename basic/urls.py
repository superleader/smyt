from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'basic.views.index', name='home'),
    url(r'^get_objects/(?P<model>\w+)$', 'basic.views.get_objects', name='get-objects'),
    url(r'^create$', 'basic.views.create', name='create-object'),
    url(r'^edit$', 'basic.views.edit', name='edit-object'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

