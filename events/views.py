from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Profile,Project,Ratings
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm,LoginForm,NewProjectForm,RatingForm
from django.views.decorators.csrf import _EnsureCsrfCookie 
from django.contrib import messages
from .serializer import ProfileSerializer,ProjectSerializer
from django.http import JsonResponse
from rest_framework import status
from .permissions import IsAdminOrReadOnly



def home(request):
   projects = Project.get_projects()
   user = request.user
   profile = Profile.get_profiles()
   return render(request, 'home.html',{"projects":projects, "user":request.user, "profile":profile})

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',{'form':form})


def login_view(request):
   if request.method == 'POST':
      form = LoginForm()
      if form.is_valid():
         username = form.cleaned_data.get('username')
         raw_password = form.cleaned_data.get('password1')
         user = authenticate(username=username, password=raw_password)
         login(request, user)
         return redirect('home')
   else:
      form = LoginForm()

   context = {
      'form': form
   }

   return render(request, 'registration/login.html', context)

def profile(request,id):
   '''
   View that allows user to view other users profiles

   '''
   user = User.objects.get(id=id)
   projects = Project.objects.all().filter(owner_id = user.id)
   profile = Profile.objects.all()
   return render(request, 'profile.html',{"projects":projects,"profile":profile,"current_user":request.user,"user":user,})

@login_required
def own_profile(request):
   '''
   Directs Current User to their own Profile.
   '''
   user = request.user    
   projects = Project.objects.all().filter(owner_id = user.id)
   profile = Profile.objects.all()
   return render(request, 'profile.html', {'projects':projects,'profile':profile, "user":user, "current_user":request.user })

@login_required
def edit_profile(request):

   user = request.user

   if request.method == 'POST':
      form = ProfileUpdateForm(request.POST,request.FILES,instance=user.profile)
      user_form = UserUpdateForm(request.POST,instance=user)
      if user_form.is_valid() and form.is_valid():
         user_form.save()
         profile = form.save(commit=False)
         profile.user = user
         profile.save()
         messages.info(request, 'You\'ve successfully updated your account!')
         return redirect('home')
   else:
      form = ProfileUpdateForm(instance=request.user)
      user_form = UserUpdateForm(instance=request.user.profile)

   context = { 
      'user': user,
      'user_form': user_form,
      'form': form
   }

   return render(request, 'edit-profile.html', context)


@login_required
def new_project(request):
    user= request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = user.profile
            project.save()
            return redirect('home')
    else:
        form = NewProjectForm()

    return render(request, 'new_project.html', {"form":form})

@login_required
def project(request, project_id):
   project = Project.get_project_id(project_id)
   ratings = Ratings.get_rating_by_projects(project_id)
   
   if request.method == 'POST':
      form = RatingForm(request.POST)
      if form.is_valid():
         ratings = form.save(commit=False)
         ratings.project = project
         ratings.user = request.user
         ratings.save()
         return redirect('project', project_id=project_id)
   else:
      form = RatingForm()
     

   return render(request, 'project.html', {'project':project, 'form':form ,'ratings':ratings})


def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        projects = Project.search_projects(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'projects':projects})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})

class ProfileList(APIView):
   def get(self,request,format=None):
      all_profiles = Profile.objects.all()
      serializers = ProfileSerializer(all_profiles, many=True)
      return Response(serializers.data)
class ProjectList(APIView):
   def get(self,request,format=None):
      all_projects = Project.objects.all()
      serializers = ProjectSerializer(all_projects, many=True)
      return Response(serializers.data)

def alerts(request):
    return render(request, 'events/templates/Alerts.html', {})


