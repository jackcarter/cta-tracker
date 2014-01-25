from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^cta/', include('cta.urls', namespace='cta')),
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
	url(r'^$', RedirectView.as_view(url='/cta/')),
)

urlpatterns += staticfiles_urlpatterns()
