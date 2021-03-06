from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from trs import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        views.HomeView.as_view(),
        name='trs.home'),
    url(r'^persons/$',
        views.PersonsView.as_view(),
        name='trs.persons'),
    url(r'^persons/(?P<slug>\w+)/$',
        views.PersonView.as_view(),
        name='trs.person'),
    url(r'^projects/$',
        views.ProjectsView.as_view(),
        name='trs.projects'),
    url(r'^projects/(?P<slug>\w+)/$',
        views.ProjectView.as_view(),
        name='trs.project'),

    url(r'^booking/$',
        views.BookingView.as_view(),
        name='trs.booking'),
    url(r'^booking/(?P<year>\d\d\d\d)-(?P<week>\d\d)/$',
        views.BookingView.as_view(),
        name='trs.booking'),
    # The one below is for single-digit week numbers. There's surely a better
    # way to do this with a regex... [Reinout]
    url(r'^booking/(?P<year>\d\d\d\d)-0(?P<week>\d)/$',
        views.BookingView.as_view(),
        name='trs.booking'),

    url(r'^login/$',
        views.LoginView.as_view(),
        name='trs.login'),
    url(r'^logout/$',
        views.logout_view,
        name='trs.logout'),

    (r'^admin/', include(admin.site.urls)),
)
