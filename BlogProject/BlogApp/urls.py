from django.urls import path
from .views import creat_user_view, get_profiles_view, get_profiles_details_view, update_profile_view, update_profile_no_form_view
urlpatterns = [
    # (EndPoint, Function, Variable to call it with)
    path('create_user/', creat_user_view, name='create-user'),
    path('profiles/', get_profiles_view, name='show-profiles'),
    path('profiles/<int:profile_id>/', get_profiles_details_view, name='profile-details'),
    path('profiles/<int:profile_id>/update/', update_profile_view, name='update-profile'),
    path('profiles/<int:profile_id>/update-no-form/', update_profile_no_form_view, name='update-profile-no-form'),
    path('create_post')
    path('posts/', post_list_view )
]
