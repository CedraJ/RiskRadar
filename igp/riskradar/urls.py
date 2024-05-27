from django.urls import path
from . import views

app_name = 'riskradar'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('assets/', views.assets_view, name='assets'),
    path('add-asset/', views.add_asset, name='add_asset'),
    path('api/assets/', views.get_assets, name='get_assets'),
    path('assets/<int:id>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<int:id>/delete/', views.asset_delete, name='asset_delete'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
]
