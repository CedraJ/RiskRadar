from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import SignUpForm, AssetForm
from .models import Asset, UserProfile
from django.contrib.auth.forms import SetPasswordForm

# Token generator instance
token_generator = PasswordResetTokenGenerator()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('riskradar:home')
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                messages.error(request, 'Invalid password.')
            else:
                messages.error(request, 'User does not exist.')
            return redirect('riskradar:login')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                user.refresh_from_db()
                
                # Ensure UserProfile is created only if it doesn't exist
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.security_question_1 = form.cleaned_data.get('security_question_1')
                profile.security_answer_1 = form.cleaned_data.get('security_answer_1')
                profile.security_question_2 = form.cleaned_data.get('security_question_2')
                profile.security_answer_2 = form.cleaned_data.get('security_answer_2')
                profile.save()
                
                messages.success(request, 'Your account has been created successfully. You can now log in.')
                return redirect('riskradar:login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'id': 'new-password'})
        self.fields['new_password2'].widget.attrs.update({'id': 'confirm-password'})

@login_required
def change_password(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "UserProfile does not exist.")
        return redirect('riskradar:profile')

    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        security_answer_1 = request.POST.get('security_answer_1')
        security_answer_2 = request.POST.get('security_answer_2')
        
        if (user_profile.security_answer_1 == security_answer_1 and
            user_profile.security_answer_2 == security_answer_2):
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important to update session to prevent logout
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('riskradar:profile')
            else:
                messages.error(request, 'Password validation failed.')
        else:
            messages.error(request, 'Security answers are incorrect.')
    else:
        form = CustomSetPasswordForm(request.user)
    
    return render(request, 'change_password.html', {
        'form': form,
        'security_question_1': user_profile.get_security_question_1_display(),
        'security_question_2': user_profile.get_security_question_2_display(),
    })

@login_required
def home_view(request):
    assets = Asset.objects.all()
    high_risk = assets.filter(risk_level='High').count()
    moderate_risk = assets.filter(risk_level='Moderate').count()
    low_risk = assets.filter(risk_level='Low').count()

    context = {
        'high_risk': high_risk,
        'moderate_risk': moderate_risk,
        'low_risk': low_risk,
    }

    return render(request, 'home.html', context)

@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('riskradar:assets')  # Redirect to the assets page
    else:
        form = AssetForm()
    return render(request, 'assets.html', {'form': form})

@login_required
def asset_edit(request, id):
    asset = get_object_or_404(Asset, pk=id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('riskradar:assets')
        else:
            return render(request, 'asset_edit.html', {'form': form, 'asset': asset})
    else:
        form = AssetForm(instance=asset)
        return render(request, 'asset_edit.html', {'form': form, 'asset': asset})

@login_required
def get_assets(request):
    assets = Asset.objects.all().values('name', 'asset_type', 'owner', 'value', 'priority', 'risk_level', 'control_measures_effectiveness', 'status')
    return JsonResponse(list(assets), safe=False)

@login_required
def asset_delete(request, id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], 'Invalid request method')
    asset = get_object_or_404(Asset, pk=id)
    asset.delete()
    return redirect('riskradar:assets')

@login_required
def assets_view(request):
    assets = Asset.objects.all()  # Fetching all assets from the database
    return render(request, 'assets.html', {'assets': assets})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user == request.user:
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('riskradar:login')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('riskradar:profile')

    return render(request, 'profile.html')

def logout_view(request):
    auth_logout(request)
    return redirect('riskradar:login')  # Redirect to login page after logout
