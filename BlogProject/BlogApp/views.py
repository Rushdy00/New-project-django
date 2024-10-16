from urllib import request

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import ProfileForm, UpdateProfileForm, PostForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import LoginView
# Create your views here.
def creat_user_view(request):
    if request.method == 'POST':
        with transaction.atomic():
            data = request.POST
            profile_picture = request.FILES.get('profile_picture')
            form = UserCreationForm(data)
            if form.is_valid():
                user_creation_data = form.cleaned_data
                user_creation_data['first_name'] = data['first_name']
                user_creation_data['last_name'] = data['last_name']
                user_creation_data['email'] = data['email']
                user_creation_data['password'] = user_creation_data.pop('password1')
                user_creation_data.pop('password2')
                user = User.objects.create_user(**user_creation_data)
                # method 1
                # Profile.objects.create(user=user, bio=data['bio'])
                # method 2

                is_employed = True if data['is_employed'] == 'on' else False
                profile = Profile(user=user, bio=data['bio'], is_employed=is_employed,
                                marital_status=data['marital_status'], profile_picture=profile_picture)
                # profile.bio = data['bio']
                profile.save()
                return HttpResponse('Profile Created Successfully')
            else:
                return HttpResponse(form.errors)
    else:
        form = UserCreationForm()
        profile_form = ProfileForm()
        return render(request, 'creat_user.html', {'form': form,
                                                                       'p': profile_form})

def get_profiles_view(request):
    profiles = Profile.objects.all()
    return render(request, 'show_profiles.html', {"profiles": profiles})

def get_profiles_details_view(request, profile_id):
    profile = Profile.objects.get(id=profile_id)

    return render(request, 'profile-detailed-view.html', {"profile": profile})

def update_profile_view(request, profile_id):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(data=request.POST)
        if profile_form.is_valid():
            data = profile_form.cleaned_data
            user_data = {}
            user_data['username'] = data.pop('username')
            user_data['first_name'] = data.pop('first_name')
            user_data['last_name'] = data.pop('last_name')
            user_data['email'] = data.pop('email')
            data['is_employed'] = True if data['is_employed'] == 'on' else False
            # profile update
            profile, created = Profile.objects.update_or_create(id=profile_id, defaults=data)
            # user update
            User.objects.update_or_create(id=profile.user.id, defaults=user_data)
            return HttpResponse('Profile Updated Successfully')
    else:
        profile = Profile.objects.get(id=profile_id)
        profile_form = UpdateProfileForm(initial={'first_name': profile.user.first_name,
                                            'last_name': profile.user.last_name,
                                            'email': profile.user.email,
                                            'bio': profile.bio,
                                            'marital_status': profile.marital_status,
                                            'is_employed': profile.is_employed,
                                            'username': profile.user.username,
                                            })
    return render(request, 'update_profile.html', {"profile": profile_form,
                                                                       'profile_id': profile.id})
def update_profile_no_form_view(request, profile_id):
    user_data = {}
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        data = request.POST.copy()
        user_data['first_name'] = data.get('first_name')
        user_data['last_name'] = data.get('last_name')
        data['is_employed'] = True if data['is_employed'] == 'on' else False
        data.pop('first_name')
        data.pop('last_name')
        # profile update
        profile, created = Profile.objects.update_or_create(id=profile_id, defaults=data)
        # profile, created = (<Profile: Mohamed>, False)
        # user update
        User.objects.update_or_create(id=profile.user.id, defaults=user_data)
        return redirect('profile-details', profile_id=profile.id)

    return render(request, 'update_profile_no_form.html', {'profile': profile})
def post_create_view(request):
    post_form = PostForm()
    return render(request, 'post_create.html', {'post': post_form})  # Fixed context dictionary
