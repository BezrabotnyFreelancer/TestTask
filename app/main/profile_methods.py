from django.shortcuts import get_object_or_404
from .models import Profile


def get_main_profile(request):
    return get_object_or_404(Profile, user=request.user)
