from django.conf.urls import url
from . import views
from django.conf import settings
# from django.contrib.auth import views as auth_views
from django.conf.urls.static import static



urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^new-project/$',views.new_project,name='new-project'),
    url(r'^project/(?P<project_id>\d+)',views.project,name='project'),
    url(r'^profile/(\d+)',views.profile,name='profile'),
    url(r'^profile',views.own_profile,name='myprofile'),
    url(r'^edit/$',views.edit_profile,name='edit_profile'),
    url(r'^search/',views.search,name='search'),
    url(r'^api/profiles/$',views.ProfileList.as_view()),
    url(r'^alerts/$', views.alerts, name='alerts'),
    url(r'^api/projects/$',views.ProjectList.as_view())
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)