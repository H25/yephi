from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.contrib import admin
from accounts.models import *

from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from registration.views import activate
from registration.views import register
from registration.forms import RegistrationForm

admin.autodiscover()

urlpatterns = patterns('',

    ##### user list and profile page #####

    url(r'^list/$',
        ListView.as_view(
            queryset = User.objects.all(),
            context_object_name = 'user_list',
            template_name = 'accounts/index.html')),
    url(r'^(?P<user_id>\d+)/$', 'accounts.views.detail'),
    url(r'^profile/$',
        'accounts.views.userprofile',
        name='user_profile'),
    url(r'^editprofile/$',
        'accounts.views.edit_profile',
        name='edit_profile'),
    url(r'^commentfeed/$', 'accounts.views.comment_feed'),

    ##### registration #####

    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        name='registration_activate'),
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^register/$',
        register,
        {'form_class' : RegistrationForm},
        name='registration_register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),

    ##### relationship request #####

    url(r'^request/$', 'accounts.views.relationship_request'),
)