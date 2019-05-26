from django.conf.urls import url
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .forms import LoginForm


urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^new-project/$', views.new_project, name='new-project'),
    url(r'^project/(?P<project_id>\d+)', views.project, name='project'),
    url(r'^profile/(\d+)',views.profile, name='profile'),
    url(r'^profile',views.own_profile, name='myprofile'),
    url(r'login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^search/', views.search, name='search'),
    url(r'^api/profiles/$',views.ProfileList.as_view()),
    url(r'^api/projects/$',views.ProjectList.as_view())
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)