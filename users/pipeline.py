

#This pipeline step extracts the picture from Google’s response and saves it to the profilePicture field. The response dictionary comes from Google’s OAuth2 API and includes the profile picture URL (e.g., https://lh3.googleusercontent.com/...).
from django.contrib.auth import get_user_model
from social_core.pipeline.partial import partial

UserAccount = get_user_model()

@partial
def save_profile_picture(strategy, details, user=None, is_new=False, *args, **kwargs):
    print("Google Response:", kwargs.get('response'))
    if user and is_new:  # Only for new users
        picture = kwargs.get('response', {}).get('picture')
        print("Profile Picture:", picture)  # Debug the picture value
          # Directly from Google's response
        if picture:
            user.profilePicture = picture
            user.save()
    elif user:  # Update existing user if picture changes
        picture = kwargs.get('response', {}).get('picture')
        if picture and user.profilePicture != picture:
            user.profilePicture = picture
            user.save()
    return {}