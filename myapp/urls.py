from django.urls import path
from .views import RegisterUserView, get_user_profile, update_user_profile
# , Edit_Profile

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    # path('user/profile/', Edit_Profile, name='edit-profile'),
    path('user/profile/', get_user_profile, name='get_user_profile'),
    path('user/profile/update/', update_user_profile, name='update_user_profile')

]